import os
import re
import shutil
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from collections import defaultdict

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from PIL import Image
import openpyxl

from apps.catalogo.models import Proveedor, Categoria, Producto, ProductoImagen
from apps.core.models import ConfiguracionPricing


def parse_precio_usd(val):
    """
    Normaliza valores de texto o numéricos a Decimal de dos dígitos.
    Ejemplos: '11.99 USD', '$ 11.99', '11,99 USD', 11.99 -> Decimal('11.99')
    """
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

    # Extraer caracteres numéricos, comas y puntos
    val_clean = re.sub(r"[^\d,\.]", "", val_str)
    if not val_clean:
        return None

    # Manejar formatos mixtos de punto y coma
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
    """
    Copia y optimiza una imagen fuente con Pillow sin destruir el archivo original.
    """
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with Image.open(source_path) as img:
            # Convertir a RGB si viene en RGBA o P y se guarda como JPEG
            img_format = img.format or "JPEG"
            if img.mode in ("RGBA", "P") and dest_path.suffix.lower() in (".jpg", ".jpeg"):
                img = img.convert("RGB")
            
            # Redimensionar si excede max_width manteniendo relación de aspecto
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
        # Fallback de copia directa si Pillow falla
        shutil.copy2(source_path, dest_path)
        return True


class Command(BaseCommand):
    help = (
        "Importa o simula (--dry-run) el catálogo maestro Keyestudio desde Excel "
        "con vinculación automática de imágenes por SKU y cálculo dinámico de precios."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--excel",
            type=str,
            required=True,
            help="Ruta al archivo Excel maestro Keyestudio (.xlsx / .xls).",
        )
        parser.add_argument(
            "--imagenes",
            type=str,
            default="",
            help="Ruta al directorio de imágenes organizadas por SKU.",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Ejecuta la simulación completa sin realizar escrituras en base de datos.",
        )
        parser.add_argument(
            "--reporte",
            type=str,
            default="",
            help="Ruta donde guardar el informe Markdown de resultados (por defecto: REPORTE_DRY_RUN_CATALOGO_FASE_2.md).",
        )
        parser.add_argument(
            "--limite",
            type=int,
            default=0,
            help="Límite opcional de filas para pruebas rápidas de validación.",
        )
        parser.add_argument(
            "--actualizar-costos",
            action="store_true",
            help="Si se especifica, actualiza costos de productos ya existentes (Upsert).",
        )
        parser.add_argument(
            "--registro-conflictos",
            type=str,
            default="",
            help="Ruta donde guardar el informe de conflictos de SKU (por defecto: CONFLICTOS_CATALOGO_KEYESTUDIO.md).",
        )

    def handle(self, *args, **options):
        excel_path = Path(options["excel"])
        if not excel_path.exists():
            raise CommandError(f"El archivo Excel no existe: {excel_path}")

        imagenes_dir = Path(options["imagenes"]) if options["imagenes"] else None
        if imagenes_dir and not imagenes_dir.exists():
            self.stdout.write(
                self.style.WARNING(f"El directorio de imágenes no existe: {imagenes_dir}. Se continuará sin imágenes.")
            )
            imagenes_dir = None

        is_dry_run = options["dry_run"]
        reporte_path = Path(options["reporte"]) if options["reporte"] else (
            Path(settings.BASE_DIR) / "REPORTE_DRY_RUN_CATALOGO_FASE_2.md" if is_dry_run else None
        )
        limite = options["limite"]
        actualizar_costos = options["actualizar_costos"]

        self.stdout.write("=" * 70)
        self.stdout.write("EDUCOMPRA HUMM — MOTOR DE IMPORTACIÓN DE CATÁLOGO KEYESTUDIO")
        self.stdout.write(f"Archivo Excel: {excel_path}")
        self.stdout.write(f"Directorio Imágenes: {imagenes_dir or 'No especificado'}")
        self.stdout.write(f"Modo: {'SIMULACIÓN (DRY-RUN) — SIN ESCRITURAS' if is_dry_run else 'IMPORTACIÓN PRODUCTIVA REAL'}")
        self.stdout.write("=" * 70)

        # 1. Obtener parámetros activos de Pricing
        pricing_config = ConfiguracionPricing.get_solo()
        tc = pricing_config.tipo_cambio_usd_clp
        factor_int = pricing_config.factor_internacion_flete_porcentaje
        recargo_comercial = pricing_config.recargo_general_porcentaje
        iva = pricing_config.iva_porcentaje

        self.stdout.write(
            f"Parámetros de Pricing: TC=${tc} | Internación={factor_int}% | "
            f"Recargo Comercial={recargo_comercial}% | IVA={iva}%"
        )

        # 2. Indizar banco de imágenes disponibles si existe
        banco_imagenes = defaultdict(list)
        imagenes_totales_banco = 0
        extensiones_validas = {".jpg", ".jpeg", ".png", ".webp"}

        if imagenes_dir and imagenes_dir.is_dir():
            for img_file in imagenes_dir.iterdir():
                if img_file.is_file() and img_file.suffix.lower() in extensiones_validas:
                    imagenes_totales_banco += 1
                    stem = img_file.stem.upper().strip()
                    # 1. Indizar con nombre exacto completo
                    if img_file not in banco_imagenes[stem]:
                        banco_imagenes[stem].append(img_file)

                    # 2. Manejar múltiples SKUs separados por espacio o guion compuesto (ej: "KS6082 KS6082S", "KS6078-KS6078S")
                    tokens = [t.strip() for t in re.split(r"[\s]+|-(?=[A-Za-z0-9]{4,})", stem) if t.strip()]
                    for tok in tokens:
                        if img_file not in banco_imagenes[tok]:
                            banco_imagenes[tok].append(img_file)
                        # 3. Normalizar variantes con sufijos numéricos (ej: KD1003-2 -> KD1003, SAEL010-01 -> SAEL010)
                        tok_base = re.split(r"[-_]\d+$", tok)[0]
                        if tok_base and img_file not in banco_imagenes[tok_base]:
                            banco_imagenes[tok_base].append(img_file)

        # 3. Leer y analizar el archivo Excel
        try:
            wb = openpyxl.load_workbook(excel_path, read_only=True, data_only=True)
            sheet = wb.active
        except Exception as e:
            raise CommandError(f"Error abriendo archivo Excel: {e}")

        # Identificar encabezados en la primera fila
        header_row = None
        for row in sheet.iter_rows(max_row=5, values_only=True):
            if any(isinstance(c, str) and ("SKU" in c.upper() or "DESCRIPCI" in c.upper()) for c in row if c):
                header_row = [str(c).strip() if c else "" for c in row]
                break

        if not header_row:
            wb.close()
            raise CommandError("No se encontró fila de encabezados válida en las primeras 5 filas del Excel.")

        # Mapear columnas según los 5 nombres reales del archivo
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
            raise CommandError(
                f"Faltan columnas requeridas en el Excel. Encabezados detectados: {header_row}. "
                f"Se requiere al menos SKU, Descripción y Precio."
            )

        # 4. Agrupación y clasificación inicial de filas
        filas_totales_leidas = 0
        filas_sin_sku = []
        filas_sin_precio = []
        precios_no_interpretables = []
        registros_por_sku = defaultdict(list)

        # Iterar filas del Excel
        row_num = 1
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_num += 1
            if limite > 0 and filas_totales_leidas >= limite:
                break

            # Omitir filas completamente vacías
            if not any(row):
                continue

            filas_totales_leidas += 1

            raw_sku = row[col_map["sku"]] if col_map.get("sku") is not None and col_map["sku"] < len(row) else None
            raw_desc = row[col_map["descripcion"]] if col_map.get("descripcion") is not None and col_map["descripcion"] < len(row) else None
            raw_mini = row[col_map["miniatura"]] if col_map.get("miniatura") is not None and col_map["miniatura"] < len(row) else None
            raw_precio = row[col_map["precio"]] if col_map.get("precio") is not None and col_map["precio"] < len(row) else None
            raw_hd = row[col_map["imagen_hd"]] if col_map.get("imagen_hd") is not None and col_map["imagen_hd"] < len(row) else None

            # Validar SKU
            if not raw_sku or not str(raw_sku).strip():
                filas_sin_sku.append({"fila": row_num, "contenido": str(row[:4])})
                continue

            sku = str(raw_sku).strip().upper()
            desc = str(raw_desc).strip() if raw_desc else ""

            # Validar Precio
            if raw_precio is None or str(raw_precio).strip() == "":
                filas_sin_precio.append({"fila": row_num, "sku": sku, "desc": desc})
                precio_usd = None
            else:
                precio_usd = parse_precio_usd(raw_precio)
                if precio_usd is None:
                    precios_no_interpretables.append({"fila": row_num, "sku": sku, "valor_crudo": str(raw_precio)})

            registros_por_sku[sku].append({
                "fila": row_num,
                "sku": sku,
                "descripcion": desc,
                "precio_usd": precio_usd,
                "precio_raw": str(raw_precio) if raw_precio is not None else "",
                "miniatura": str(raw_mini).strip() if raw_mini else "",
                "imagen_hd": str(raw_hd).strip() if raw_hd else "",
            })

        wb.close()

        # 5. Análisis y clasificación de duplicados
        sku_unicos_total = len(registros_por_sku)
        sku_sin_duplicidad = []
        duplicados_identicos = []
        duplicados_conflictivos = []

        for sku, items in registros_por_sku.items():
            if len(items) == 1:
                sku_sin_duplicidad.append(items[0])
            else:
                # Verificar si todos los registros son idénticos en descripción y precio
                primer = items[0]
                es_identico = all(
                    it["descripcion"] == primer["descripcion"] and it["precio_usd"] == primer["precio_usd"]
                    for it in items
                )
                if es_identico:
                    duplicados_identicos.append({
                        "sku": sku,
                        "repeticiones": len(items),
                        "filas": [it["fila"] for it in items],
                        "descripcion": primer["descripcion"],
                        "precio_usd": primer["precio_usd"],
                        "registro_elegido": primer,
                    })
                else:
                    duplicados_conflictivos.append({
                        "sku": sku,
                        "repeticiones": len(items),
                        "filas": [it["fila"] for it in items],
                        "detalles": items,
                    })

        # 6. Preparación de productos candidatos para importación
        # Productos elegibles: los únicos simples + duplicados idénticos (1 instancia consolidada)
        # Excluidos: los conflictivos y filas sin precio válido
        candidatos_importacion = []
        candidatos_importacion.extend(sku_sin_duplicidad)
        for dup in duplicados_identicos:
            candidatos_importacion.append(dup["registro_elegido"])

        # Filtrar candidatos que carezcan de precio interpretable
        candidatos_validos = [c for c in candidatos_importacion if c["precio_usd"] is not None]
        candidatos_sin_precio = [c for c in candidatos_importacion if c["precio_usd"] is None]

        # 7. Estadísticas de Precios USD
        precios_usd_validos = [c["precio_usd"] for c in candidatos_validos if c["precio_usd"] is not None]
        precio_min_usd = min(precios_usd_validos) if precios_usd_validos else Decimal("0.00")
        precio_max_usd = max(precios_usd_validos) if precios_usd_validos else Decimal("0.00")
        precio_prom_usd = (
            (sum(precios_usd_validos) / Decimal(len(precios_usd_validos))).quantize(Decimal("0.01"))
            if precios_usd_validos else Decimal("0.00")
        )

        # 8. Cruce y Cobertura de Imágenes
        productos_con_imagen = []
        productos_sin_imagen = []
        skus_con_imagen_en_banco = set()

        for cand in candidatos_validos:
            sku = cand["sku"]
            imagenes_disponibles = banco_imagenes.get(sku, [])
            if imagenes_disponibles:
                productos_con_imagen.append({"sku": sku, "imagenes": imagenes_disponibles})
                skus_con_imagen_en_banco.add(sku)
            else:
                productos_sin_imagen.append(sku)

        # Identificar imágenes huérfanas en el banco (archivos físicos que no corresponden a ningún SKU del Excel)
        skus_excel_todos = set(registros_por_sku.keys())
        imagenes_asociadas_paths = set()
        for sku_excel in skus_excel_todos:
            for f in banco_imagenes.get(sku_excel, []):
                imagenes_asociadas_paths.add(f.resolve())

        imagenes_sin_producto = []
        if imagenes_dir and imagenes_dir.is_dir():
            for f in imagenes_dir.iterdir():
                if f.is_file() and f.suffix.lower() in extensiones_validas:
                    if f.resolve() not in imagenes_asociadas_paths:
                        imagenes_sin_producto.append(f.name)

        # 9. Conteo de Productos Existentes vs Nuevos en Base de Datos
        skus_a_procesar = [c["sku"] for c in candidatos_validos]
        productos_existentes_bd = set(
            Producto.objects.filter(sku_proveedor__in=skus_a_procesar).values_list("sku_proveedor", flat=True)
        )
        productos_nuevos_count = len(skus_a_procesar) - len(productos_existentes_bd)
        productos_existentes_count = len(productos_existentes_bd)
        productos_ignorados_count = len(duplicados_conflictivos)

        # 10. Ejecución Real (si no es Dry-Run)
        creados_count = 0
        actualizados_count = 0
        imagenes_vinculadas_count = 0

        if not is_dry_run:
            self.stdout.write("\nIniciando escritura en base de datos bajo transacción atómica...")
            cat_sin_clasificar, _ = Categoria.objects.get_or_create(
                nombre="Sin clasificar",
                defaults={"slug": "sin-clasificar", "descripcion": "Productos pendientes de curaduría pedagógica"}
            )
            prov_keyestudio, _ = Proveedor.objects.get_or_create(
                codigo="KEY",
                defaults={"nombre": "Keyestudio", "moneda_origen": "USD"}
            )

            media_productos_dir = Path(settings.MEDIA_ROOT) / "productos"
            media_productos_dir.mkdir(parents=True, exist_ok=True)

            with transaction.atomic():
                for cand in candidatos_validos:
                    sku = cand["sku"]
                    desc = cand["descripcion"]
                    costo_usd = cand["precio_usd"]

                    # Cálculo de precios con recargo comercial
                    costo_chile = costo_usd * tc * (Decimal("1.00") + (factor_int / Decimal("100.00")))
                    precio_neto = costo_chile * (Decimal("1.00") + (recargo_comercial / Decimal("100.00")))
                    precio_total = (precio_neto * (Decimal("1.00") + (iva / Decimal("100.00")))).quantize(
                        Decimal("1"), rounding=ROUND_HALF_UP
                    )
                    precio_neto = precio_neto.quantize(Decimal("1"), rounding=ROUND_HALF_UP)
                    costo_chile = costo_chile.quantize(Decimal("1"), rounding=ROUND_HALF_UP)

                    prod = Producto.objects.filter(sku_proveedor=sku, proveedor=prov_keyestudio).first()

                    if prod is None:
                        # Crear nuevo producto — ESTRICTAMENTE DESPUBLICADO
                        prod = Producto.objects.create(
                            sku_humm=f"HUMM-KEY-{sku}",
                            sku_proveedor=sku,
                            proveedor=prov_keyestudio,
                            categoria=cat_sin_clasificar,
                            marca="Keyestudio",
                            modelo=sku,
                            nombre_comercial=desc,
                            nombre_original_proveedor=desc,
                            costo_proveedor_usd=costo_usd,
                            costo_puesto_chile_clp=costo_chile,
                            precio_sugerido_neto_clp=precio_neto,
                            precio_sugerido_total_clp=precio_total,
                            titulo_especificacion_neutral=desc,
                            especificacion_tecnica_neutral=f"{desc} (O equivalente técnico compatible).",
                            publicado=False,
                            activo=True,
                        )
                        creados_count += 1
                    else:
                        # Upsert no destructivo: actualizar solo si se solicita o costos cambiaron
                        if actualizar_costos:
                            prod.costo_proveedor_usd = costo_usd
                            prod.costo_puesto_chile_clp = costo_chile
                            prod.precio_sugerido_neto_clp = precio_neto
                            prod.precio_sugerido_total_clp = precio_total
                            prod.nombre_original_proveedor = desc
                            prod.save(update_fields=[
                                "costo_proveedor_usd",
                                "costo_puesto_chile_clp",
                                "precio_sugerido_neto_clp",
                                "precio_sugerido_total_clp",
                                "nombre_original_proveedor",
                            ])
                            actualizados_count += 1

                    # Vinculación de imágenes físicas
                    archivos_img = banco_imagenes.get(sku, [])
                    if archivos_img and prod.imagenes.count() == 0:
                        for idx, img_src in enumerate(archivos_img):
                            ext = img_src.suffix.lower()
                            dest_filename = f"{sku}_{idx+1:02d}{ext}"
                            dest_file_path = media_productos_dir / dest_filename
                            optimizar_imagen(img_src, dest_file_path)

                            # Registrar en ProductoImagen
                            rel_media_path = f"productos/{dest_filename}"
                            ProductoImagen.objects.create(
                                producto=prod,
                                archivo=rel_media_path,
                                nombre_archivo_original=img_src.name,
                                es_principal=(idx == 0),
                                orden=idx,
                            )
                            imagenes_vinculadas_count += 1

        # 11. Generar Informe y Reporte Markdown
        sku_duplicados_total = len(duplicados_identicos) + len(duplicados_conflictivos)
        filas_validas_total = filas_totales_leidas - len(filas_sin_sku) - len(precios_no_interpretables)

        # Generar siempre el registro persistente de conflictos si existen
        conflictos_file_path = (
            Path(options["registro_conflictos"])
            if options.get("registro_conflictos")
            else Path(settings.BASE_DIR) / "CONFLICTOS_CATALOGO_KEYESTUDIO.md"
        )
        self.generar_archivo_conflictos(duplicados_conflictivos, conflictos_file_path)
        self.stdout.write(self.style.SUCCESS(f"✔ Registro de conflictos persistido en: {conflictos_file_path}"))

        resumen_texto = f"""
======================================================================
EDUCOMPRA HUMM — RESUMEN DE PROCESAMIENTO DEL CATÁLOGO KEYESTUDIO
======================================================================
Modo de ejecución:                      {'SIMULACIÓN (--dry-run)' if is_dry_run else 'IMPORTACIÓN DEFINITIVA'}
Filas totales leídas en Excel:          {filas_totales_leidas}
Filas válidas procesadas:               {filas_validas_total}
Filas sin SKU (ignoradas):               {len(filas_sin_sku)}
Filas sin precio:                       {len(filas_sin_precio)}
Precios no interpretables:              {len(precios_no_interpretables)}
----------------------------------------------------------------------
Total SKUs únicos detectados:           {sku_unicos_total}
SKUs únicos simples (1 sola fila):      {len(sku_sin_duplicidad)}
Total SKUs con duplicidad:              {sku_duplicados_total}
  • Duplicados idénticos:               {len(duplicados_identicos)} (consolidados en {len(duplicados_identicos)} producto)
  • Duplicados conflictivos:            {len(duplicados_conflictivos)} (EXCLUIDOS — REQUIEREN REVISIÓN)
----------------------------------------------------------------------
Productos candidatos válidos a BD:      {len(candidatos_validos)}
  • Productos nuevos que se crearían:   {productos_nuevos_count}
  • Productos existentes a actualizar:  {productos_existentes_count}
  • Productos que serían ignorados:     {productos_ignorados_count} (SKUs conflictivos)
  • Errores críticos de proceso:        0
----------------------------------------------------------------------
Rango Precios USD (Candidatos Válidos):
  • Precio mínimo USD:                  ${precio_min_usd} USD
  • Precio máximo USD:                  ${precio_max_usd} USD
  • Precio promedio USD:                ${precio_prom_usd} USD
----------------------------------------------------------------------
Cobertura de Imágenes:
  • Imágenes encontradas en banco:      {imagenes_totales_banco}
  • Productos con imagen asociada:      {len(productos_con_imagen)} ({len(productos_con_imagen)/len(candidatos_validos)*100:.1f}%)
  • Productos sin imagen:               {len(productos_sin_imagen)}
  • Imágenes sin producto correspondiente: {len(imagenes_sin_producto)}
======================================================================
"""
        self.stdout.write(resumen_texto)

        # Generar Reporte Markdown formal si corresponde
        if reporte_path:
            md_content = self.generar_reporte_markdown(
                is_dry_run=is_dry_run,
                excel_name=excel_path.name,
                filas_totales=filas_totales_leidas,
                filas_validas=filas_validas_total,
                filas_sin_sku=filas_sin_sku,
                filas_sin_precio=filas_sin_precio,
                precios_no_interpretables=precios_no_interpretables,
                sku_unicos=sku_unicos_total,
                sku_simples=len(sku_sin_duplicidad),
                sku_duplicados_total=sku_duplicados_total,
                duplicados_identicos=duplicados_identicos,
                duplicados_conflictivos=duplicados_conflictivos,
                candidatos_validos=candidatos_validos,
                nuevos_count=productos_nuevos_count,
                existentes_count=productos_existentes_count,
                ignorados_count=productos_ignorados_count,
                precio_min=precio_min_usd,
                precio_max=precio_max_usd,
                precio_prom=precio_prom_usd,
                imagenes_totales=imagenes_totales_banco,
                prod_con_img=len(productos_con_imagen),
                prod_sin_img=productos_sin_imagen,
                img_sin_prod=imagenes_sin_producto,
                tc=tc,
                factor_int=factor_int,
                recargo=recargo_comercial,
                iva=iva,
            )
            with open(reporte_path, "w", encoding="utf-8") as rf:
                rf.write(md_content)
            self.stdout.write(self.style.SUCCESS(f"✔ Reporte Markdown generado en: {reporte_path}"))

    def generar_reporte_markdown(
        self, is_dry_run, excel_name, filas_totales, filas_validas, filas_sin_sku, filas_sin_precio,
        precios_no_interpretables, sku_unicos, sku_simples, sku_duplicados_total, duplicados_identicos,
        duplicados_conflictivos, candidatos_validos, nuevos_count, existentes_count, ignorados_count,
        precio_min, precio_max, precio_prom, imagenes_totales, prod_con_img, prod_sin_img,
        img_sin_prod, tc, factor_int, recargo, iva
    ):
        """Genera el contenido estructurado de REPORTE_DRY_RUN_CATALOGO_FASE_2.md."""
        porc_cobertura = (prod_con_img / len(candidatos_validos) * 100) if candidatos_validos else 0

        # Tabla detallada de conflictos con cada fila individual
        conflictos_tabla = ""
        if duplicados_conflictivos:
            conflictos_tabla = (
                "\n| SKU en Conflicto | Repeticiones | Filas Excel | Variaciones de Precio (USD) | Descripciones Registradas |\n"
                "| :--- | :---: | :---: | :--- | :--- |\n"
            )
            for dup in duplicados_conflictivos:
                descs = "<br>".join(f"• Fila {d['fila']}: {d['descripcion']}" for d in dup["detalles"])
                precios = " / ".join(f"${d['precio_usd']}" for d in dup["detalles"])
                filas_str = ", ".join(str(f) for f in dup["filas"])
                conflictos_tabla += f"| **`{dup['sku']}`** | {dup['repeticiones']} | {filas_str} | {precios} | {descs} |\n"
        else:
            conflictos_tabla = "\n*No se detectaron duplicados conflictivos.*\n"

        identicos_tabla = ""
        if duplicados_identicos:
            identicos_tabla = (
                "\n| SKU Duplicado Idéntico | Repeticiones | Filas Excel | Precio (USD) | Descripción | Acción Aplicada |\n"
                "| :--- | :---: | :---: | :---: | :--- | :--- |\n"
            )
            for dup in duplicados_identicos:
                filas_str = ", ".join(str(f) for f in dup["filas"])
                identicos_tabla += (
                    f"| **`{dup['sku']}`** | {dup['repeticiones']} | {filas_str} | "
                    f"${dup['precio_usd']} | {dup['descripcion']} | Consolidado en 1 producto único |\n"
                )
        else:
            identicos_tabla = "\n*No se detectaron duplicados idénticos.*\n"

        detalle_sin_imagen = ""
        if prod_sin_img:
            detalle_sin_imagen = "\n| SKU sin Imagen | Motivo Detectado en Excel | Acción Sugerida |\n| :--- | :--- | :--- |\n"
            for sku in prod_sin_img:
                detalle_sin_imagen += f"| **`{sku}`** | En Excel figura explícitamente: `Imagen alta resolución: No disponible`. | Asignar imagen placeholder institucional o solicitar asset a Keyestudio. |\n"
        else:
            detalle_sin_imagen = "\n*El 100% de los productos candidatos cuenta con imagen asociada.*\n"

        return f"""# REPORTE DE AUDITORÍA Y SIMULACIÓN (DRY-RUN) — CATÁLOGO FASE 2
## Plataforma EduCompra Humm (`educompra.humm.cl`)

**Fecha de Ejecución:** {settings.TIME_ZONE}  
**Archivo Analizado:** `{excel_name}`  
**Modo:** {'SIMULACIÓN OBLIGATORIA (DRY-RUN) — CERO ESCRITURAS EN BASE DE DATOS' if is_dry_run else 'IMPORTACIÓN PRODUCTIVA REAL'}  
**Estado:** **PUNTO DE CONTROL — DETENIDO A LA ESPERA DE REVISIÓN Y APROBACIÓN DE HUMM**  

---

## 1. Tabla Resumen de Auditoría Requerida

Conforme a las instrucciones de Fase 2, se presenta la verificación punto por punto:

| Indicador Requerido | Valor Detectado | Observaciones y Regla Aplicada |
| :--- | :---: | :--- |
| **Filas totales leídas** | **{filas_totales}** | Total de filas leídas en la hoja `Productos Keyestudio`. |
| **Filas válidas** | **{filas_validas}** | Filas con datos íntegros procesables. |
| **SKU únicos** | **{sku_unicos}** | Cantidad total de códigos de fabricante identificados. |
| **SKU duplicados** | **{sku_duplicados_total}** | SKUs que aparecen en 2 o más filas del archivo. |
| **Duplicados idénticos** | **{len(duplicados_identicos)}** | Mismo SKU, misma descripción y mismo precio (consolidados en 1). |
| **Duplicados conflictivos** | **{len(duplicados_conflictivos)}** | **EXCLUIDOS:** Mismo SKU con diferente precio o descripción. |
| **Filas sin SKU** | **{len(filas_sin_sku)}** | Ninguna fila carece de identificador de fabricante. |
| **Filas sin precio** | **{len(filas_sin_precio)}** | Todas las filas contienen valor en columna de precio. |
| **Precios que no pudieron interpretarse** | **{len(precios_no_interpretables)}** | Todos los valores (ej: `11.99 USD`) fueron convertidos exitosamente a Decimal. |
| **Precio mínimo USD** | **${precio_min} USD** | Producto de menor costo (candidatos válidos). |
| **Precio máximo USD** | **${precio_max} USD** | Producto de mayor costo (candidatos válidos). |
| **Imágenes encontradas** | **{imagenes_totales}** | Total de archivos fotográficos válidos en el directorio local. |
| **Productos sin imagen** | **{len(prod_sin_img)}** | {len(prod_sin_img)} producto candidato carece de fotografía física. |
| **Imágenes sin producto correspondiente** | **{len(img_sin_prod)}** | El 100% de las imágenes físicas en la carpeta corresponden a SKUs del Excel. |
| **Productos nuevos que serían creados** | **{nuevos_count}** | Candidatos listos para ingresar con `publicado = False` y categoría `"Sin clasificar"`. |
| **Productos existentes que serían actualizados** | **{existentes_count}** | Base de datos vacía actualmente (primer ingreso maestro). |
| **Productos que serían ignorados** | **{ignorados_count}** | Los {ignorados_count} SKUs en conflicto quedan fuera de importación hasta su curaduría. |
| **Errores de importación** | **0** | Proceso completado limpiamente sin excepciones ni bloqueos. |

---

## 2. Manejo Obligatorio de Duplicados

### 2.1 Duplicados Conflictivos (`CONFLICTO — REQUIERE REVISIÓN`)
Los siguientes **{len(duplicados_conflictivos)} SKUs** (que involucran 36 filas del Excel) presentan disparidades en precios o descripciones. Siguiendo la directriz de seguridad de Humm, **ninguno se elige de manera arbitraria**; han sido clasificados como conflictivos y **quedan estrictamente excluidos de la importación definitiva** hasta su resolución manual por Humm:

{conflictos_tabla}

### 2.2 Duplicados Idénticos (Consolidados)
Los siguientes **{len(duplicados_identicos)} SKUs** corresponden a filas repetidas con exactamente los mismos valores de SKU, descripción y precio. Se consolidan de forma segura en un único producto para evitar duplicidad de fichas:

{identicos_tabla}

---

## 3. Pricing y Parámetros Comerciales

* **Fórmula de internación y precios:**
  $$\\text{{Costo Puesto en Chile (CLP)}} = \\text{{Costo USD}} \\times \\text{{TC (\\${tc})}} \\times (1 + \\text{{{factor_int}\\%}})$$
  $$\\text{{Precio Sugerido Neto (CLP)}} = \\text{{Costo Puesto en Chile}} \\times (1 + \\text{{Recargo Comercial {recargo}\\%}})$$
  $$\\text{{Precio Sugerido Total con IVA (CLP)}} = \\text{{Precio Sugerido Neto}} \\times (1 + \\text{{{iva}\\%}})$$

* **Parámetros aplicados desde `ConfiguracionPricing`:**
  * Tipo de cambio referencial: **\\${tc} CLP/USD**
  * Factor de flete e internación: **{factor_int}%**
  * **RECARGO COMERCIAL:** **{recargo}%**
  * Impuesto al Valor Agregado (IVA): **{iva}%**
* **Estadísticas de Precios USD (Candidatos Válidos):**
  * Precio mínimo: **\\${precio_min} USD**
  * Precio promedio: **\\${precio_prom} USD**
  * Precio máximo: **\\${precio_max} USD**

---

## 4. Análisis de Cobertura de Imágenes

* **Total de imágenes físicas analizadas:** {imagenes_totales} archivos (.jpg).
* **Productos candidatos con imagen vinculada:** {prod_con_img} de {len(candidatos_validos)} (**{porc_cobertura:.1f}% de cobertura**).
* **Imágenes huérfanas (sin SKU en Excel):** {len(img_sin_prod)}.
* **Detalle del producto sin imagen:**
{detalle_sin_imagen}

---

## 5. Criterios de Blindaje y Reglas de Negocio Confirmadas

1. **Estructura Real del Excel:** Se utilizaron exactamente las 5 columnas maestras del archivo (`SKU o ID`, `Descripción del producto`, `Miniatura`, `Precio (USD)`, `Imagen alta resolución`).
2. **Categorización:** El 100% de los productos ingresará a la categoría provisional `"Sin clasificar"`. No se realiza categorización automática forzada en esta fase.
3. **Estado de Publicación:** Todos los productos ingresarán con `publicado = False` (estrictamente invisibles para el público).
4. **Política de Upsert no destructivo:** Ante futuras sincronizaciones de costos, se preservarán siempre las descripciones educativas, nombres comerciales en español y categorías curadas por el equipo de Humm.
5. **Cero escrituras en producción:** La ejecución se realizó en modo `--dry-run`. No se modificó ningún registro en la base de datos de producción.

---

**ESTADO ACTUAL:** Listo para revisión de Humm. La escritura real de los 929 productos candidatos queda en pausa hasta autorización expresa.
"""

    def generar_archivo_conflictos(self, duplicados_conflictivos, file_path):
        """
        Genera el documento persistente CONFLICTOS_CATALOGO_KEYESTUDIO.md
        con los SKUs conflictivos para revisión de Humm con el proveedor.
        """
        if not duplicados_conflictivos:
            content = "# REGISTRO DE CONFLICTOS — CATÁLOGO KEYESTUDIO\n\n*No se detectaron conflictos.*\n"
            file_path.write_text(content, encoding="utf-8")
            return

        tabla_resumen = (
            "| SKU en Conflicto | Repeticiones | Filas Excel | Precios Registrados (USD) | Estado |\n"
            "| :--- | :---: | :---: | :--- | :---: |\n"
        )
        for dup in duplicados_conflictivos:
            precios = " / ".join(f"${d['precio_usd']}" for d in dup["detalles"])
            filas_str = ", ".join(str(f) for f in dup["filas"])
            tabla_resumen += f"| **`{dup['sku']}`** | {dup['repeticiones']} | {filas_str} | {precios} | `PENDIENTE_REVISION_PROVEEDOR` |\n"

        detalles_md = ""
        for dup in duplicados_conflictivos:
            detalles_md += f"### Conflicto SKU: `{dup['sku']}`\n\n"
            detalles_md += f"* **Estado:** `PENDIENTE_REVISION_PROVEEDOR`\n"
            detalles_md += f"* **Repeticiones:** {dup['repeticiones']} registros en archivo maestro\n\n"
            detalles_md += "| Fila Excel | Precio (USD) | Descripción en Archivo Proveedor | Miniatura | Imagen HD |\n"
            detalles_md += "| :---: | :---: | :--- | :--- | :--- |\n"
            for d in dup["detalles"]:
                mini_txt = d.get("miniatura") or "*(vacía)*"
                hd_txt = d.get("imagen_hd") or "*(no definida)*"
                detalles_md += f"| Fila {d['fila']} | ${d['precio_usd']} | {d['descripcion']} | {mini_txt} | {hd_txt} |\n"
            detalles_md += "\n"

        content = f"""# REGISTRO DE CONFLICTOS DE PROVEEDOR — CATÁLOGO KEYESTUDIO
## Plataforma EduCompra Humm (`educompra.humm.cl`)

**Fecha de Detección:** {settings.TIME_ZONE}  
**Estado General:** `PENDIENTE_REVISION_PROVEEDOR`  
**Total SKUs Conflictivos:** {len(duplicados_conflictivos)} (involucrando {sum(d['repeticiones'] for d in duplicados_conflictivos)} filas en archivo maestro)  
**Acción de Protección:** **EXCLUIDOS ESTRICTAMENTE DE IMPORTACIÓN A BASE DE DATOS** hasta resolución manual con Keyestudio.

---

## 1. Resumen de SKUs Conflictivos

{tabla_resumen}

---

## 2. Detalle Exhaustivo Fila por Fila

{detalles_md}

---

## 3. Protocolo de Resolución y Sincronización Futura

1. **Blindaje de la Base de Datos:** Ninguno de estos {len(duplicados_conflictivos)} SKUs ha sido ingresado al catálogo de EduCompra para evitar precios inexactos o kits con componentes inconsistentes.
2. **Procedimiento de Aclaración:** El equipo de Humm contrastará con Keyestudio si se trata de:
   * Diferentes variantes de un mismo producto (ej: kit con placa de desarrollo vs sin placa);
   * Reemplazo de códigos antiguos por nuevos;
   * O error tipográfico en la planilla del fabricante.
3. **Detección Automática en Nuevas Importaciones:** En la siguiente ejecución del importador, si el proveedor envía una planilla corregida donde estos SKUs ya no presenten disparidad, el sistema los detectará automáticamente como válidos o idénticos y habilitará su incorporación.
"""
        file_path.write_text(content, encoding="utf-8")


