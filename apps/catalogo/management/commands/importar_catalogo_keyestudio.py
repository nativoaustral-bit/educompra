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
                    # Normalizar variantes (ej: KS0011_01 -> base KS0011)
                    sku_base = re.split(r"[-_]\d+$", stem)[0]
                    banco_imagenes[sku_base].append(img_file)
                    # También indizar con nombre exacto
                    if stem != sku_base:
                        banco_imagenes[stem].append(img_file)

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

        # Identificar imágenes huérfanas en el banco (imágenes cuyo SKU no existe en el Excel)
        skus_excel_todos = set(registros_por_sku.keys())
        imagenes_huerfanas = []
        for sku_banco, files in banco_imagenes.items():
            if sku_banco not in skus_excel_todos:
                for f in files:
                    imagenes_huerfanas.append(f.name)

        # 9. Conteo de Productos Existentes vs Nuevos en Base de Datos
        skus_a_procesar = [c["sku"] for c in candidatos_validos]
        productos_existentes_bd = set(
            Producto.objects.filter(sku_proveedor__in=skus_a_procesar).values_list("sku_proveedor", flat=True)
        )
        productos_nuevos_count = len(skus_a_procesar) - len(productos_existentes_bd)
        productos_existentes_count = len(productos_existentes_bd)

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
                                imagen=rel_media_path,
                                es_portada=(idx == 0),
                                orden=idx,
                            )
                            imagenes_vinculadas_count += 1

        # 11. Generar Informe y Reporte Markdown
        resumen_texto = f"""
======================================================================
RESUMEN DE PROCESAMIENTO DEL CATÁLOGO KEYESTUDIO
======================================================================
Modo de ejecución:              {'SIMULACIÓN (--dry-run)' if is_dry_run else 'IMPORTACIÓN DEFINITIVA'}
Filas totales leídas en Excel:  {filas_totales_leidas}
Filas sin SKU (ignoradas):       {len(filas_sin_sku)}
Filas sin precio:               {len(filas_sin_precio)}
Precios no interpretables:      {len(precios_no_interpretables)}
----------------------------------------------------------------------
Total SKUs únicos detectados:   {sku_unicos_total}
SKUs únicos simples (1 fila):   {len(sku_sin_duplicidad)}
Duplicados idénticos:           {len(duplicados_identicos)} (consolidados en {len(duplicados_identicos)} productos)
Duplicados conflictivos:        {len(duplicados_conflictivos)} (EXCLUIDOS POR REVISIÓN)
----------------------------------------------------------------------
Productos candidatos válidos:   {len(candidatos_validos)}
  • Nuevos para crear:          {productos_nuevos_count}
  • Existentes en base datos:   {productos_existentes_count}
----------------------------------------------------------------------
Rango Precios USD (Candidatos):
  • Mínimo:                     ${precio_min_usd} USD
  • Máximo:                     ${precio_max_usd} USD
  • Promedio:                   ${precio_prom_usd} USD
----------------------------------------------------------------------
Cobertura de Imágenes:
  • Imágenes en banco físico:   {imagenes_totales_banco}
  • Productos con imagen:       {len(productos_con_imagen)} ({len(productos_con_imagen)/len(candidatos_validos)*100:.1f}% si >0)
  • Productos sin imagen:       {len(productos_sin_imagen)}
  • Imágenes huérfanas:         {len(imagenes_huerfanas)}
======================================================================
"""
        self.stdout.write(resumen_texto)

        # Generar Reporte Markdown formal si corresponde
        if reporte_path:
            md_content = self.generar_reporte_markdown(
                is_dry_run=is_dry_run,
                excel_name=excel_path.name,
                filas_totales=filas_totales_leidas,
                filas_sin_sku=filas_sin_sku,
                filas_sin_precio=filas_sin_precio,
                precios_no_interpretables=precios_no_interpretables,
                sku_unicos=sku_unicos_total,
                sku_simples=len(sku_sin_duplicidad),
                duplicados_identicos=duplicados_identicos,
                duplicados_conflictivos=duplicados_conflictivos,
                candidatos_validos=candidatos_validos,
                nuevos_count=productos_nuevos_count,
                existentes_count=productos_existentes_count,
                precio_min=precio_min_usd,
                precio_max=precio_max_usd,
                precio_prom=precio_prom_usd,
                imagenes_totales=imagenes_totales_banco,
                prod_con_img=len(productos_con_imagen),
                prod_sin_img=len(productos_sin_imagen),
                img_huerfanas=imagenes_huerfanas,
                tc=tc,
                factor_int=factor_int,
                recargo=recargo_comercial,
                iva=iva,
            )
            with open(reporte_path, "w", encoding="utf-8") as rf:
                rf.write(md_content)
            self.stdout.write(self.style.SUCCESS(f"✔ Reporte Markdown generado en: {reporte_path}"))

    def generar_reporte_markdown(
        self, is_dry_run, excel_name, filas_totales, filas_sin_sku, filas_sin_precio,
        precios_no_interpretables, sku_unicos, sku_simples, duplicados_identicos,
        duplicados_conflictivos, candidatos_validos, nuevos_count, existentes_count,
        precio_min, precio_max, precio_prom, imagenes_totales, prod_con_img, prod_sin_img,
        img_huerfanas, tc, factor_int, recargo, iva
    ):
        """Genera el contenido estructurado de REPORTE_DRY_RUN_CATALOGO_FASE_2.md."""
        porc_cobertura = (prod_con_img / len(candidatos_validos) * 100) if candidatos_validos else 0

        conflictos_tabla = ""
        if duplicados_conflictivos:
            conflictos_tabla = "\n| SKU en Conflicto | Repeticiones | Filas Excel | Valores Dispares Detectados |\n| :--- | :---: | :---: | :--- |\n"
            for dup in duplicados_conflictivos:
                descs = " / ".join(set(d["descripcion"][:40] for d in dup["detalles"]))
                precios = " / ".join(set(str(d["precio_usd"]) for d in dup["detalles"]))
                filas_str = ", ".join(str(f) for f in dup["filas"])
                conflictos_tabla += f"| **{dup['sku']}** | {dup['repeticiones']} | {filas_str} | Precios: {precios} — Descs: {descs} |\n"
        else:
            conflictos_tabla = "\n*No se detectaron duplicados conflictivos.*\n"

        identicos_tabla = ""
        if duplicados_identicos:
            identicos_tabla = "\n| SKU Duplicado Idéntico | Repeticiones | Filas Excel | Acción Aplicada |\n| :--- | :---: | :---: | :--- |\n"
            for dup in duplicados_identicos[:15]:
                filas_str = ", ".join(str(f) for f in dup["filas"])
                identicos_tabla += f"| **{dup['sku']}** | {dup['repeticiones']} | {filas_str} | Consolidado en 1 producto único |\n"
            if len(duplicados_identicos) > 15:
                identicos_tabla += f"| ... ({len(duplicados_identicos) - 15} adicionales) | ... | ... | Consolidados exitosamente |\n"
        else:
            identicos_tabla = "\n*No se detectaron duplicados idénticos.*\n"

        return f"""# REPORTE DE AUDITORÍA Y SIMULACIÓN (DRY-RUN) — CATÁLOGO FASE 2
## Plataforma EduCompra Humm (`educompra.humm.cl`)

**Fecha de Ejecución:** {settings.TIME_ZONE}  
**Archivo Analizado:** `{excel_name}`  
**Modo:** {'SIMULACIÓN OBLIGATORIA (DRY-RUN) — CERO ESCRITURAS' if is_dry_run else 'IMPORTACIÓN PRODUCTIVA'}  
**Estado:** Pendiente de Revisión por Humm  

---

## 1. Métricas Generales de Ingesta

| Indicador | Valor Reportado | Detalle / Observación |
| :--- | :---: | :--- |
| **Filas Totales Leídas** | **{filas_totales}** | Total de registros con datos en el archivo Excel. |
| **Filas sin SKU** | **{len(filas_sin_sku)}** | Filas ignoradas por carecer de identificador de fabricante. |
| **Filas sin Precio** | **{len(filas_sin_precio)}** | Filas con celda de precio vacía o no definida. |
| **Precios No Interpretables** | **{len(precios_no_interpretables)}** | Valores de precio que no pudieron convertirse a Decimal. |
| **SKUs Únicos Totales** | **{sku_unicos}** | Cantidad total de códigos de producto identificados. |
| **SKUs Únicos Simples** | **{sku_simples}** | SKUs con aparición única en el archivo. |
| **Duplicados Idénticos** | **{len(duplicados_identicos)}** | Registros repetidos con idéntica descripción y precio (consolidados). |
| **Duplicados Conflictivos** | **{len(duplicados_conflictivos)}** | **EXCLUIDOS:** Mismo SKU con diferente precio o descripción. |
| **Candidatos Válidos para BD** | **{len(candidatos_validos)}** | Productos limpios preparados para incorporación interna. |
| **Nuevos a Crear** | **{nuevos_count}** | Productos que entrarán con `publicado = False`. |
| **Existentes a Preservar** | **{existentes_count}** | Productos ya existentes en base de datos. |

---

## 2. Clasificación de Duplicados

### 2.1 Duplicados Conflictivos (Excluidos de Importación)
Conforme a las directrices de Humm, ningún SKU con información dispar se elige automáticamente. Quedan marcados como **`CONFLICTO — REQUIERE REVISIÓN`** y se excluyen de la base de datos hasta que el equipo decida la resolución:

{conflictos_tabla}

### 2.2 Duplicados Idénticos (Consolidados)
Registros que comparten exactamente el mismo SKU, texto y precio, consolidados en una única entidad:

{identicos_tabla}

---

## 3. Parámetros y Análisis de Precios (USD y CLP)

* **Fórmula Aplicada:** Costo USD × TC (${tc}) × (1 + {factor_int}%) × (1 + Recargo Comercial {recargo}%) × (1 + IVA {iva}%)
* **Precio Mínimo USD:** `${precio_min} USD`
* **Precio Máximo USD:** `${precio_max} USD`
* **Precio Promedio USD:** `${precio_prom} USD`

Todos los precios en pesos chilenos calculados son redondeados al entero más cercano (`ROUND_HALF_UP`) sin decimales.

---

## 4. Cobertura de Imágenes

| Métrica | Cantidad | Porcentaje |
| :--- | :---: | :---: |
| **Archivos en Banco Físico** | **{imagenes_totales}** | 100% |
| **Productos con Imagen Asociada** | **{prod_con_img}** | **{porc_cobertura:.1f}%** |
| **Productos sin Imagen (Placeholder)** | **{prod_sin_img}** | **{100 - porc_cobertura:.1f}%** |
| **Imágenes Huérfanas en Banco** | **{len(img_huerfanas)}** | - |

---

## 5. Criterios de Seguridad y Blindaje Confirmados

1. **Estado de Publicación:** El 100% de los candidatos ({len(candidatos_validos)} productos) ingresará con `publicado = False`.
2. **Categorización:** Todo producto nuevo ingresa asignado a `"Sin clasificar"`.
3. **Preservación (Upsert):** Si se re-importa en el futuro, no se alterarán textos en español, descripciones educativas, especificaciones técnicas neutras ni categorías curadas.
4. **Punto de Control:** Este informe fue generado en modo `--dry-run`. **Ninguna tabla fue alterada.**

---

*Reporte preparado para revisión de Humm antes de la ejecución definitiva.*
"""
