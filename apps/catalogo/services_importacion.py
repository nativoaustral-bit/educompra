"""
Motor unificado de importación masiva de catálogo Keyestudio (Ajustes #10, #11, #12, #20 y #21 de Humm).
Servicio reutilizado idénticamente por la CLI (importar_catalogo_keyestudio) y por la interfaz web (/gestion/importaciones/).
"""

import os
import re
import shutil
import zipfile
from collections import defaultdict
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import transaction
from PIL import Image
import openpyxl

from apps.catalogo.models import Proveedor, Categoria, Producto, ProductoImagen, PrecioProveedorTramo
from apps.core.models import ConfiguracionPricing
from apps.gestion.services_auditoria import registrar_actividad


def parse_precio_usd(val):
    """Normaliza valores de texto o numéricos a Decimal de dos dígitos."""
    if val is None:
        return None
    if isinstance(val, (int, float, Decimal)):
        try:
            return Decimal(str(val)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except (InvalidOperation, ValueError):
            return None

    val_str = str(val).strip()
    if not val_str:
        return None

    val_clean = re.sub(r"[^\d,\.]", "", val_str)
    if not val_clean:
        return None

    if "," in val_clean and "." in val_clean:
        if val_clean.rfind(".") > val_clean.rfind(","):
            val_clean = val_clean.replace(",", "")
        else:
            val_clean = val_clean.replace(".", "").replace(",", ".")
    elif "," in val_clean:
        val_clean = val_clean.replace(",", ".")

    try:
        return Decimal(val_clean).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except (InvalidOperation, ValueError):
        return None


def optimizar_imagen(source_path, dest_path, max_width=1200, quality=85):
    """Copia y optimiza una imagen fuente con Pillow sin destruir el archivo original."""
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(source_path) as img:
            if img.mode in ("RGBA", "P") and dest_path.suffix.lower() in (".jpg", ".jpeg"):
                img = img.convert("RGB")
            
            if img.width > max_width:
                height = int(img.height * (max_width / img.width))
                img = img.resize((max_width, height), Image.Resampling.LANCZOS)

            save_kwargs = {}
            if dest_path.suffix.lower() in (".jpg", ".jpeg"):
                save_kwargs = {"quality": quality, "optimize": True}
            elif dest_path.suffix.lower() == ".webp":
                save_kwargs = {"quality": quality}
            
            img.save(dest_path, **save_kwargs)
            return True
    except Exception:
        shutil.copy2(source_path, dest_path)
        return True


class ImportacionCatalogoService:
    # Límites de seguridad para archivos subidos (Ajuste Obligatorio #11)
    MAX_EXCEL_BYTES = 15 * 1024 * 1024       # 15 MB
    MAX_ZIP_BYTES = 50 * 1024 * 1024         # 50 MB
    MAX_ZIP_UNCOMPRESSED = 150 * 1024 * 1024 # 150 MB
    MAX_ZIP_FILES = 2000
    EXTENSIONES_IMAGEN_VALIDAS = {".jpg", ".jpeg", ".png", ".webp"}

    @classmethod
    def validar_archivo_excel(cls, archivo_path):
        """Valida tamaño y formato del archivo Excel."""
        p = Path(archivo_path)
        if not p.exists():
            raise ValidationError(f"El archivo Excel no existe: {p}")
        if p.suffix.lower() not in (".xlsx", ".xls"):
            raise ValidationError("El archivo debe tener extensión .xlsx o .xls.")
        if p.stat().st_size > cls.MAX_EXCEL_BYTES:
            raise ValidationError(f"El archivo Excel excede el tamaño máximo permitido de {cls.MAX_EXCEL_BYTES // (1024*1024)} MB.")
        return True

    @classmethod
    def validar_y_descomprimir_zip(cls, zip_path, destino_dir):
        """
        Valida exhaustivamente un archivo ZIP para prevenir ZIP bombs, path traversal
        y archivos maliciosos antes de extraer (Ajuste Obligatorio #11).
        """
        p = Path(zip_path)
        if not p.exists():
            raise ValidationError("El archivo ZIP no existe.")
        if p.stat().st_size > cls.MAX_ZIP_BYTES:
            raise ValidationError(f"El archivo ZIP excede el tamaño máximo de {cls.MAX_ZIP_BYTES // (1024*1024)} MB.")

        destino = Path(destino_dir)
        destino.mkdir(parents=True, exist_ok=True)

        total_size = 0
        total_files = 0

        with zipfile.ZipFile(p, "r") as zf:
            for member in zf.infolist():
                # Prevenir path traversal (../ o rutas absolutas)
                norm_name = os.path.normpath(member.filename)
                if norm_name.startswith("..") or os.path.isabs(norm_name):
                    raise ValidationError(f"Entrada ZIP sospechosa (path traversal): {member.filename}")

                if member.is_dir():
                    continue

                total_files += 1
                if total_files > cls.MAX_ZIP_FILES:
                    raise ValidationError(f"El archivo ZIP contiene más de {cls.MAX_ZIP_FILES} archivos (límite de seguridad).")

                total_size += member.file_size
                if total_size > cls.MAX_ZIP_UNCOMPRESSED:
                    raise ValidationError(f"El contenido descomprimido excede el límite de {cls.MAX_ZIP_UNCOMPRESSED // (1024*1024)} MB (posible ZIP bomb).")

                # Validar extensión interna
                ext = Path(member.filename).suffix.lower()
                if ext not in cls.EXTENSIONES_IMAGEN_VALIDAS:
                    continue  # Omitir archivos no imagen sin fallar

                # Extracción segura
                target_path = destino / Path(member.filename).name
                with zf.open(member) as source, open(target_path, "wb") as target:
                    shutil.copyfileobj(source, target)

        return destino

    FORMATO_MAESTRO_ANTIGUO = "FORMATO_MAESTRO_ANTIGUO"
    FORMATO_LISTA_COMERCIAL_NUEVA = "FORMATO_LISTA_COMERCIAL_NUEVA"

    SKUS_CONFLICTIVOS_HISTORICOS = {
        "KS0077", "KS0078", "KS0079", "KS0240", "KS0080",
        "KS0081", "KS0082", "KS0400", "KS0401", "60720227",
        "KS0801", "KS4031", "KS4032", "KS0536", "KS0537"
    }

    @classmethod
    def detectar_formato(cls, sheet):
        """
        Analiza las primeras 15 filas de la hoja para determinar si corresponde a:
        - FORMATO_LISTA_COMERCIAL_NUEVA (Contiene columnas de volumen Q1-9, Q10-49, etc.)
        - FORMATO_MAESTRO_ANTIGUO (Catálogo maestro original con SKU o ID, Descripción, Precio USD)
        """
        for row in sheet.iter_rows(max_row=15, values_only=True):
            if not row or not any(row):
                continue
            row_strs = [str(c).upper().strip() for c in row if c is not None]
            row_concat = " ".join(row_strs)

            if any("Q1-9" in s or "Q1 - 9" in s or "Q1_9" in s for s in row_strs) or "Q1-9" in row_concat:
                return cls.FORMATO_LISTA_COMERCIAL_NUEVA

            if any("SKU" in s for s in row_strs) and any("DESCRIPC" in s or "PRECIO" in s for s in row_strs):
                return cls.FORMATO_MAESTRO_ANTIGUO

        raise ValidationError("No se detectó un formato reconocido en las primeras 15 filas de la planilla.")

    @classmethod
    def validar_tramos_volumen(cls, q1_9, q10_49, q50_100, q101_300):
        """
        Valida la monotonicidad lógica decreciente de los tramos de precio por volumen.
        Regla comercial: Q1-9 >= Q10-49 >= Q50-100 >= Q101-300.
        Si un tramo de mayor volumen es superior al tramo anterior, se marca como
        PRECIO_PROVEEDOR_REQUIERE_REVISION y se aísla de uso automático.
        """
        tramos_def = [
            (1, 9, q1_9, "Q1-9"),
            (10, 49, q10_49, "Q10-49"),
            (50, 100, q50_100, "Q50-100"),
            (101, 300, q101_300, "Q101-300"),
        ]
        tramos_resultado = []
        anomalias = []
        tiene_anomalia = False

        ultimo_precio_valido = None
        for min_cant, max_cant, precio, etiqueta in tramos_def:
            if precio is None:
                continue
            es_anomalo = False
            estado_val = "VALIDADO"
            notas = ""

            if precio <= Decimal("0.00"):
                es_anomalo = True
                estado_val = "PRECIO_PROVEEDOR_REQUIERE_REVISION"
                notas = f"Precio en tramo {etiqueta} no es positivo (USD ${precio})."
                anomalias.append(notas)
                tiene_anomalia = True
            elif ultimo_precio_valido is not None and precio > ultimo_precio_valido:
                es_anomalo = True
                estado_val = "PRECIO_PROVEEDOR_REQUIERE_REVISION"
                notas = f"Anomalía en {etiqueta}: precio USD ${precio} excede el tramo previo (${ultimo_precio_valido})."
                anomalias.append(notas)
                tiene_anomalia = True
            else:
                ultimo_precio_valido = precio

            tramos_resultado.append({
                "cantidad_minima": min_cant,
                "cantidad_maxima": max_cant,
                "precio_usd": precio,
                "es_anomalo": es_anomalo,
                "estado_validacion": estado_val,
                "notas_validacion": notas,
                "etiqueta": etiqueta,
            })

        return tramos_resultado, tiene_anomalia, anomalias

    @classmethod
    def sincronizar_imagenes_banco(cls, skus, imagenes_dir="data_import/imagenes"):
        """
        Escanea el banco físico de imágenes y vincula automáticamente cualquier fotografía
        existente a los productos indicados por sku_proveedor.

        Reglas:
        - Admite extensiones: .jpg, .jpeg, .png, .webp
        - No reemplaza ni duplica imágenes ya vinculadas correctamente
        - Optimiza la imagen y la almacena en el media persistente (media/productos/)
        - Crea ProductoImagen marcando es_principal=True
        - NO modifica: costos, precios, tramos, nombres, categorías, curaduría,
          especificación neutral ni estado de publicación (mantiene publicado=False)
        - Retorna reporte detallado por SKU
        """
        imagenes_p = Path(imagenes_dir) if imagenes_dir else Path("data_import/imagenes")
        if not imagenes_p.exists() or not imagenes_p.is_dir():
            raise ValidationError(f"El directorio de imágenes {imagenes_dir} no existe.")

        # Indizar banco físico de imágenes
        banco_imagenes = defaultdict(list)
        for img_file in imagenes_p.iterdir():
            if img_file.is_file() and img_file.suffix.lower() in cls.EXTENSIONES_IMAGEN_VALIDAS:
                stem = img_file.stem.upper().strip()
                if img_file not in banco_imagenes[stem]:
                    banco_imagenes[stem].append(img_file)
                tokens = [t.strip() for t in re.split(r"[\s]+|-(?=[A-Za-z0-9]{4,})", stem) if t.strip()]
                for tok in tokens:
                    if img_file not in banco_imagenes[tok]:
                        banco_imagenes[tok].append(img_file)

        media_productos_dir = Path(settings.MEDIA_ROOT) / "productos"
        media_productos_dir.mkdir(parents=True, exist_ok=True)
        media_catalogo_dir = Path(settings.MEDIA_ROOT) / "catalogo" / "originales"
        media_catalogo_dir.mkdir(parents=True, exist_ok=True)

        reporte = []

        for sku in skus:
            sku_clean = str(sku).strip().upper()
            prod = (
                Producto.objects.filter(sku_proveedor__iexact=sku_clean).first()
                or Producto.objects.filter(sku_humm__iexact=sku_clean).first()
            )

            if not prod:
                reporte.append({
                    "sku": sku_clean,
                    "archivo_encontrado": "N/A (Producto no existe en BD)",
                    "imagen_vinculada": False,
                    "estado": "ERROR_PRODUCTO_NO_ENCONTRADO",
                })
                continue

            # Si ya tiene imagen, no reemplazar ni duplicar
            if prod.imagenes.exists():
                img_actual = prod.imagenes.first()
                reporte.append({
                    "sku": sku_clean,
                    "archivo_encontrado": img_actual.nombre_archivo_original or Path(img_actual.archivo.name).name,
                    "imagen_vinculada": False,
                    "estado": "YA_VINCULADA",
                })
                continue

            # Buscar archivos en banco físico
            archivos_img = banco_imagenes.get(sku_clean, [])
            if not archivos_img:
                for ext in cls.EXTENSIONES_IMAGEN_VALIDAS:
                    cand = imagenes_p / f"{sku_clean}{ext}"
                    if cand.exists() and cand.is_file():
                        archivos_img.append(cand)
                        break

            if not archivos_img:
                reporte.append({
                    "sku": sku_clean,
                    "archivo_encontrado": "Ninguno",
                    "imagen_vinculada": False,
                    "estado": "SIN_IMAGEN",
                })
                continue

            # Imagen encontrada -> procesar y vincular
            img_src = archivos_img[0]
            ext = img_src.suffix.lower()
            dest_filename = f"{prod.sku_proveedor}_01{ext}"
            dest_path_prod = media_productos_dir / dest_filename
            dest_path_cat = media_catalogo_dir / img_src.name

            # Optimizar y copiar al media persistente
            optimizar_imagen(img_src, dest_path_prod)
            optimizar_imagen(img_src, dest_path_cat)

            # Crear ProductoImagen
            rel_media_path = f"productos/{dest_filename}"
            ProductoImagen.objects.create(
                producto=prod,
                archivo=rel_media_path,
                nombre_archivo_original=img_src.name,
                es_principal=True,
                orden=0,
            )

            reporte.append({
                "sku": sku_clean,
                "archivo_encontrado": img_src.name,
                "imagen_vinculada": True,
                "estado": "OK",
            })

        return reporte

    @classmethod
    def procesar_catalogo(cls, excel_path, imagenes_dir=None, is_dry_run=True,
                          actualizar_costos=True, limite=0, usuario=None, lote=None, request=None,
                          skus_filtro=None):
        """
        Ejecuta el procesamiento integral del catálogo:
        - Detecta automáticamente el formato (Maestro original o Lista comercial nueva con tramos)
        - Soporta --dry-run (sin modificaciones en base de datos)
        - Soporta filtro específico por lista de SKUs
        - Valida tramos de precios por volumen y monotonicidad
        - Detecta SKUs únicos y conflictivos
        - Preserva estrictamente la curaduría existente (Ajuste #18)
        - Aplica nuevos productos con publicado=False y SIN_REVISAR (Ajuste #17)
        - Retorna reporte consolidado estructurado
        """
        excel_p = Path(excel_path)
        cls.validar_archivo_excel(excel_p)

        imagenes_p = Path(imagenes_dir) if imagenes_dir else None
        if imagenes_p and not imagenes_p.exists():
            imagenes_p = None

        skus_filtro_set = {str(s).strip().upper() for s in skus_filtro} if skus_filtro else None

        # 1. Parámetros de Pricing (sin escrituras en dry-run)
        if is_dry_run:
            pricing_config = ConfiguracionPricing.objects.filter(pk=1).first() or ConfiguracionPricing()
        else:
            pricing_config = ConfiguracionPricing.get_solo()
        tc = pricing_config.tipo_cambio_usd_clp
        factor_int = pricing_config.factor_internacion_flete_porcentaje
        recargo_comercial = pricing_config.recargo_general_porcentaje
        iva = pricing_config.iva_porcentaje

        # 2. Indizar banco de imágenes
        banco_imagenes = defaultdict(list)
        imagenes_totales_banco = 0
        if imagenes_p and imagenes_p.is_dir():
            for img_file in imagenes_p.iterdir():
                if img_file.is_file() and img_file.suffix.lower() in cls.EXTENSIONES_IMAGEN_VALIDAS:
                    imagenes_totales_banco += 1
                    stem = img_file.stem.upper().strip()
                    if img_file not in banco_imagenes[stem]:
                        banco_imagenes[stem].append(img_file)
                    tokens = [t.strip() for t in re.split(r"[\s]+|-(?=[A-Za-z0-9]{4,})", stem) if t.strip()]
                    for tok in tokens:
                        if img_file not in banco_imagenes[tok]:
                            banco_imagenes[tok].append(img_file)
                        tok_base = re.split(r"[-_]\d+$", tok)[0]
                        if tok_base and img_file not in banco_imagenes[tok_base]:
                            banco_imagenes[tok_base].append(img_file)

        # 3. Leer Excel y detectar formato
        wb = openpyxl.load_workbook(excel_p, data_only=True)
        sheet = wb.active

        formato_detectado = cls.detectar_formato(sheet)

        filas_totales_leidas = 0
        filas_sin_sku = 0
        filas_sin_precio = 0
        precios_no_interpretables = 0
        registros_por_sku = defaultdict(list)

        if formato_detectado == cls.FORMATO_MAESTRO_ANTIGUO:
            header_row = None
            header_row_idx = 1
            for idx, row in enumerate(sheet.iter_rows(max_row=10, values_only=True), start=1):
                if any(isinstance(c, str) and ("SKU" in c.upper() or "DESCRIPCI" in c.upper()) for c in row if c):
                    header_row = [str(c).strip() if c else "" for c in row]
                    header_row_idx = idx
                    break

            if not header_row:
                wb.close()
                raise ValidationError("No se encontró fila de encabezados válida en el catálogo maestro.")

            col_map = {}
            for idx, col in enumerate(header_row):
                col_upper = col.upper()
                if "SKU" in col_upper or "ID" in col_upper:
                    col_map["sku"] = idx
                elif "DESCRIPCI" in col_upper or "PRODUCTO" in col_upper:
                    col_map["descripcion"] = idx
                elif "MINIATURA" in col_upper:
                    col_map["miniatura"] = idx
                elif "PRECIO" in col_upper:
                    col_map["precio"] = idx
                elif "ALTA RESOLUCI" in col_upper or "IMAGEN ALTA" in col_upper:
                    col_map["imagen_hd"] = idx

            if "sku" not in col_map or "descripcion" not in col_map or "precio" not in col_map:
                wb.close()
                raise ValidationError(f"Faltan columnas requeridas (SKU, Descripción, Precio) en formato maestro.")

            for row in sheet.iter_rows(min_row=header_row_idx + 1, values_only=True):
                if limite > 0 and filas_totales_leidas >= limite:
                    break
                if not any(row):
                    continue
                filas_totales_leidas += 1

                raw_sku = row[col_map["sku"]] if col_map["sku"] < len(row) else None
                raw_desc = row[col_map["descripcion"]] if col_map["descripcion"] < len(row) else None
                raw_precio = row[col_map["precio"]] if col_map["precio"] < len(row) else None

                if not raw_sku or not str(raw_sku).strip():
                    filas_sin_sku += 1
                    continue
                if raw_precio is None or str(raw_precio).strip() == "":
                    filas_sin_precio += 1
                    continue

                sku_norm = str(raw_sku).strip().upper()
                if skus_filtro_set and sku_norm not in skus_filtro_set:
                    continue

                precio_usd = parse_precio_usd(raw_precio)
                if precio_usd is None or precio_usd <= Decimal("0.00"):
                    precios_no_interpretables += 1
                    continue

                desc_norm = str(raw_desc).strip() if raw_desc else ""
                tramos_base = [{
                    "cantidad_minima": 1,
                    "cantidad_maxima": None,
                    "precio_usd": precio_usd,
                    "es_anomalo": False,
                    "estado_validacion": "VALIDADO",
                    "notas_validacion": "",
                    "etiqueta": "Base (1+)",
                }]

                registros_por_sku[sku_norm].append({
                    "sku": sku_norm,
                    "nombre": desc_norm,
                    "descripcion": desc_norm,
                    "features": "",
                    "precio_usd": precio_usd,
                    "q1_9": precio_usd,
                    "q10_49": None,
                    "q50_100": None,
                    "q101_300": None,
                    "tramos": tramos_base,
                    "tiene_anomalia_precio": False,
                    "anomalias_detalle": [],
                })

        elif formato_detectado == cls.FORMATO_LISTA_COMERCIAL_NUEVA:
            col_map = {}
            for row in sheet.iter_rows(values_only=True):
                if limite > 0 and filas_totales_leidas >= limite:
                    break
                if not row or not any(row):
                    continue

                # Filtrar filas que solo sean títulos de sección (ej: "HOT PRODUCTS", "FOR ARDUINO")
                celdas_con_valor = [c for c in row if c is not None and str(c).strip()]
                if len(celdas_con_valor) <= 1:
                    continue

                # Verificar si es una fila de encabezados repetida
                fila_strs = [str(c).upper().strip() if c is not None else "" for c in row]
                if any("SKU" in s for s in fila_strs) and any("Q1-9" in s or "Q1 - 9" in s or "PRODUCT" in s for s in fila_strs):
                    # Actualizar mapeo de columnas
                    col_map = {}
                    for idx, s in enumerate(fila_strs):
                        if "SKU" in s:
                            col_map["sku"] = idx
                        elif "PRODUCT" in s or "NAME" in s or "DESCRIPCI" in s:
                            col_map["nombre"] = idx
                        elif "FEATURE" in s:
                            col_map["features"] = idx
                        elif "Q1-9" in s or "Q1 - 9" in s or "Q1_9" in s:
                            col_map["q1_9"] = idx
                        elif "Q10-49" in s or "Q10 - 49" in s or "Q10_49" in s:
                            col_map["q10_49"] = idx
                        elif "Q50-100" in s or "Q50 - 100" in s or "Q50_100" in s:
                            col_map["q50_100"] = idx
                        elif "Q101-300" in s or "Q101 - 300" in s or "Q101_300" in s:
                            col_map["q101_300"] = idx
                    continue

                if "sku" not in col_map or "q1_9" not in col_map:
                    continue

                raw_sku = row[col_map["sku"]] if col_map["sku"] < len(row) else None
                if not raw_sku or not str(raw_sku).strip():
                    filas_sin_sku += 1
                    continue

                sku_clean = str(raw_sku).strip().upper()
                if sku_clean == "SKU":
                    continue

                filas_totales_leidas += 1

                if skus_filtro_set and sku_clean not in skus_filtro_set:
                    continue

                raw_name = str(row[col_map["nombre"]]).strip() if "nombre" in col_map and col_map["nombre"] < len(row) and row[col_map["nombre"]] is not None else ""
                raw_features = str(row[col_map["features"]]).strip() if "features" in col_map and col_map["features"] < len(row) and row[col_map["features"]] is not None else ""

                raw_q1_9 = row[col_map["q1_9"]] if "q1_9" in col_map and col_map["q1_9"] < len(row) else None
                raw_q10_49 = row[col_map["q10_49"]] if "q10_49" in col_map and col_map["q10_49"] < len(row) else None
                raw_q50_100 = row[col_map["q50_100"]] if "q50_100" in col_map and col_map["q50_100"] < len(row) else None
                raw_q101_300 = row[col_map["q101_300"]] if "q101_300" in col_map and col_map["q101_300"] < len(row) else None

                p_q1_9 = parse_precio_usd(raw_q1_9)
                p_q10_49 = parse_precio_usd(raw_q10_49)
                p_q50_100 = parse_precio_usd(raw_q50_100)
                p_q101_300 = parse_precio_usd(raw_q101_300)

                if p_q1_9 is None or p_q1_9 <= Decimal("0.00"):
                    filas_sin_precio += 1
                    precios_no_interpretables += 1
                    continue

                tramos_res, tiene_anomalia, anomalias = cls.validar_tramos_volumen(p_q1_9, p_q10_49, p_q50_100, p_q101_300)

                registros_por_sku[sku_clean].append({
                    "sku": sku_clean,
                    "nombre": raw_name,
                    "descripcion": raw_name,
                    "features": raw_features,
                    "precio_usd": p_q1_9,
                    "q1_9": p_q1_9,
                    "q10_49": p_q10_49,
                    "q50_100": p_q50_100,
                    "q101_300": p_q101_300,
                    "tramos": tramos_res,
                    "tiene_anomalia_precio": tiene_anomalia,
                    "anomalias_detalle": anomalias,
                })

        wb.close()

        # 4. Análisis de duplicados y conflictos
        skus_simples = {}
        skus_duplicados_identicos = {}
        skus_conflictivos = {}

        for sku, items in registros_por_sku.items():
            if len(items) == 1:
                skus_simples[sku] = items[0]
            else:
                precios = {it["precio_usd"] for it in items}
                if len(precios) == 1:
                    skus_duplicados_identicos[sku] = items[0]
                else:
                    skus_conflictivos[sku] = items

        candidatos_validos = {**skus_simples, **skus_duplicados_identicos}

        # 5. Comparar contra base de datos existente
        skus_existentes_qs = Producto.objects.filter(sku_proveedor__in=candidatos_validos.keys()).select_related("categoria")
        existentes_map = {p.sku_proveedor: p for p in skus_existentes_qs}

        productos_nuevos_count = 0
        productos_actualizados_costo = 0
        productos_sin_cambios = 0
        conflictos_count = len(skus_conflictivos)
        anomalias_precio_count = 0
        productos_sin_imagen = 0
        imagenes_asociadas = 0

        precios_usd_validos = [c["precio_usd"] for c in candidatos_validos.values()]
        precio_min = min(precios_usd_validos) if precios_usd_validos else Decimal("0.00")
        precio_max = max(precios_usd_validos) if precios_usd_validos else Decimal("0.00")
        precio_prom = sum(precios_usd_validos) / len(precios_usd_validos) if precios_usd_validos else Decimal("0.00")

        detalle_skus = []

        # Verificación no destructiva de dependencias
        dependencias_faltantes = []
        prov = Proveedor.objects.filter(codigo="KEY").first()
        cat_sin_clasificar = Categoria.objects.filter(nombre="Sin clasificar").first()

        if not prov:
            dependencias_faltantes.append("DEPENDENCIA_FALTANTE: Proveedor KEY (Keyestudio)")
        if not cat_sin_clasificar:
            dependencias_faltantes.append("DEPENDENCIA_FALTANTE: Categoría 'Sin clasificar'")

        for sku, data in candidatos_validos.items():
            prod_existente = existentes_map.get(sku)
            tiene_img = bool(banco_imagenes.get(sku)) or (prod_existente.imagenes.exists() if prod_existente else False)
            if data.get("tiene_anomalia_precio"):
                anomalias_precio_count += 1

            costo_ant = prod_existente.costo_proveedor_usd if prod_existente else None
            q1_9_val = data["precio_usd"]
            diff_costo = (q1_9_val - costo_ant) if costo_ant is not None else None
            diff_pct = ((diff_costo / costo_ant) * 100) if (costo_ant and costo_ant > 0) else None

            es_historico = sku in cls.SKUS_CONFLICTIVOS_HISTORICOS

            if sku == "KS0540":
                accion_prop = (
                    "Actualizar costos y tramos de proveedor + preparar curaduría Humm prioritaria: "
                    "'Kit Inicial Arduino con Placa Controladora — 20 Proyectos Guiados' "
                    "(Categoría: Kits educativos iniciales, Nivel: INICIAL, diferenciándolo explícitamente "
                    "de KS0541 que no incluye placa controladora)."
                )
            elif prod_existente:
                if prod_existente.publicado:
                    accion_prop = "Actualizar información de proveedor y tramos de volumen preservando estrictamente curaduría Humm y publicación."
                else:
                    accion_prop = "Actualizar información de proveedor y tramos de volumen + mantener en catálogo interno para curaduría pedagógica."
            else:
                accion_prop = "Crear nuevo registro (activo=True, publicado=False, estado_curaduria='SIN_REVISAR', placeholder SIN_IMAGEN) + registrar tramos de volumen."

            if es_historico:
                accion_prop = f"[ALERTA CONFLICTO HISTÓRICO] {accion_prop}"

            if prod_existente:
                estado_actual = "EXISTENTE / PUBLICADO" if prod_existente.publicado else "EXISTENTE / NO PUBLICADO"
            else:
                estado_actual = "NUEVO SKU (NO EXISTE EN BD)"

            if es_historico:
                estado_actual += " [CONFLICTO HISTÓRICO]"

            detalle_skus.append({
                "sku": sku,
                "nombre_proveedor": data.get("nombre", ""),
                "features": data.get("features", ""),
                "existe": prod_existente is not None,
                "publicado": prod_existente.publicado if prod_existente else False,
                "estado_curaduria": prod_existente.estado_curaduria if prod_existente else "SIN_REVISAR",
                "estado_actual": estado_actual,
                "costo_anterior": float(costo_ant) if costo_ant is not None else None,
                "q1_9": float(q1_9_val),
                "q10_49": float(data["q10_49"]) if data.get("q10_49") is not None else None,
                "q50_100": float(data["q50_100"]) if data.get("q50_100") is not None else None,
                "q101_300": float(data["q101_300"]) if data.get("q101_300") is not None else None,
                "diferencia_costo": float(diff_costo) if diff_costo is not None else None,
                "diferencia_porcentaje": round(float(diff_pct), 1) if diff_pct is not None else None,
                "conflicto_historico": es_historico,
                "tiene_anomalia_precio": data.get("tiene_anomalia_precio", False),
                "anomalias_detalle": data.get("anomalias_detalle", []),
                "accion_propuesta": accion_prop,
                "tiene_imagen_banco": tiene_img,
            })

            if prod_existente:
                if prod_existente.costo_proveedor_usd != data["precio_usd"]:
                    productos_actualizados_costo += 1
                else:
                    productos_sin_cambios += 1
            else:
                productos_nuevos_count += 1

            if tiene_img:
                imagenes_asociadas += 1
            else:
                productos_sin_imagen += 1

        # 6. Ejecución definitiva si no es dry-run
        if not is_dry_run:
            with transaction.atomic():
                # Creación segura de dependencias dentro de la transacción definitiva
                prov, _ = Proveedor.objects.get_or_create(
                    codigo="KEY",
                    defaults={"nombre": "Keyestudio", "moneda_origen": "USD"}
                )
                cat_sin_clasificar, _ = Categoria.objects.get_or_create(
                    nombre="Sin clasificar",
                    defaults={"descripcion": "Componentes pendientes de curaduría pedagógica"}
                )

                for sku, data in candidatos_validos.items():
                    prod_existente = existentes_map.get(sku)
                    if prod_existente:
                        # Actualizar información de proveedor sin alterar curaduría Humm (Ajuste #18)
                        prod_existente.nombre_original_proveedor = data.get("nombre") or prod_existente.nombre_original_proveedor
                        if data.get("features"):
                            prod_existente.features_proveedor = data["features"]
                        if actualizar_costos and prod_existente.costo_proveedor_usd != data["precio_usd"]:
                            prod_existente.costo_proveedor_usd = data["precio_usd"]
                        prod_existente.save()
                        prod_target = prod_existente
                    else:
                        prod_nuevo = Producto(
                            sku_humm=f"HUMM-KEY-{sku}",
                            sku_proveedor=sku,
                            proveedor=prov,
                            categoria=cat_sin_clasificar,
                            marca="Keyestudio",
                            nombre_comercial=data.get("nombre") or f"Componente Keyestudio {sku}",
                            nombre_original_proveedor=data.get("nombre") or "",
                            features_proveedor=data.get("features") or "",
                            costo_proveedor_usd=data["precio_usd"],
                            publicado=False,
                            activo=True,
                            estado_curaduria="SIN_REVISAR",
                            estado_especificacion_neutral="NO_REVISADO",
                        )
                        prod_nuevo.save()
                        prod_target = prod_nuevo

                    # Registrar/actualizar tramos de volumen de proveedor
                    for tramo in data.get("tramos", []):
                        if tramo.get("precio_usd") is not None:
                            PrecioProveedorTramo.objects.update_or_create(
                                producto=prod_target,
                                proveedor=prov,
                                cantidad_minima=tramo["cantidad_minima"],
                                defaults={
                                    "cantidad_maxima": tramo.get("cantidad_maxima"),
                                    "precio_usd": tramo["precio_usd"],
                                    "es_anomalo": tramo.get("es_anomalo", False),
                                    "estado_validacion": tramo.get("estado_validacion", "VALIDADO"),
                                    "notas_validacion": tramo.get("notas_validacion", ""),
                                }
                            )

                    # Manejo de imágenes (sin sobrescribir existentes)
                    archivos_img = banco_imagenes.get(sku, [])
                    if archivos_img and not prod_target.imagenes.exists():
                        for idx, img_src in enumerate(archivos_img[:5]):
                            dest_media = Path(settings.MEDIA_ROOT) / "catalogo" / "originales" / img_src.name
                            optimizar_imagen(img_src, dest_media)
                            ProductoImagen.objects.create(
                                producto=prod_target,
                                archivo=f"catalogo/originales/{img_src.name}",
                                nombre_archivo_original=img_src.name,
                                es_principal=(idx == 0),
                                orden=idx,
                            )

        # Resumen estructurado
        resumen = {
            "formato_detectado": formato_detectado,
            "is_dry_run": is_dry_run,
            "dependencias_faltantes": dependencias_faltantes,
            "estado_dependencias": "DEPENDENCIA_FALTANTE" if dependencias_faltantes else "OK",
            "total_filas": filas_totales_leidas,
            "filas_totales_leidas": filas_totales_leidas,
            "filas_sin_sku": filas_sin_sku,
            "filas_sin_precio": filas_sin_precio,
            "precios_no_interpretables": precios_no_interpretables,
            "skus_detectados": len(registros_por_sku),
            "skus_simples": len(skus_simples),
            "skus_duplicados_identicos": len(skus_duplicados_identicos),
            "conflictos_detectados": conflictos_count,
            "anomalias_precio_detectadas": anomalias_precio_count,
            "productos_candidatos": len(candidatos_validos),
            "productos_nuevos": productos_nuevos_count,
            "productos_actualizados": productos_actualizados_costo,
            "productos_sin_cambios": productos_sin_cambios,
            "precio_min_usd": float(precio_min),
            "precio_max_usd": float(precio_max),
            "precio_prom_usd": float(precio_prom),
            "imagenes_encontradas_banco": imagenes_totales_banco,
            "productos_con_imagen": imagenes_asociadas,
            "productos_sin_imagen": productos_sin_imagen,
            "skus_conflictivos_lista": [
                {"sku": k, "filas": v} for k, v in list(skus_conflictivos.items())[:20]
            ],
            "detalle_skus": detalle_skus,
        }

        # Actualizar lote en BD si existe
        if lote:
            lote.filas_leidas = filas_totales_leidas
            lote.skus_detectados = len(registros_por_sku)
            lote.productos_nuevos = productos_nuevos_count
            lote.productos_actualizados = productos_actualizados_costo
            lote.productos_sin_cambios = productos_sin_cambios
            lote.conflictos_detectados = conflictos_count
            lote.productos_sin_imagen = productos_sin_imagen
            lote.resumen_json = resumen
            if is_dry_run:
                lote.estado = "CON_CONFLICTOS" if conflictos_count > 0 else "SIMULADO"
            else:
                lote.estado = "APLICADO"
                lote.es_dry_run = False
            lote.save()

        # Auditoría si fue definitivo
        if not is_dry_run:
            registrar_actividad(
                request=request,
                accion="IMPORTACION_EJECUTADA",
                modelo_afectado="Producto",
                objeto_id=lote.id if lote else "",
                descripcion=f"Importación de catálogo ejecutada: {productos_nuevos_count} nuevos, {productos_actualizados_costo} costos actualizados.",
                detalles={
                    "formato": formato_detectado,
                    "nuevos": productos_nuevos_count,
                    "costos_actualizados": productos_actualizados_costo,
                    "sin_cambios": productos_sin_cambios,
                    "conflictos": conflictos_count,
                }
            )

        return resumen

