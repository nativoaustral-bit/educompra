"""
Comando de auditoría automática de integridad del catálogo público (Fase 4B).
Compara los 72 productos activos y publicados contra CATALOGO_CURADO_FASE_3.md
en los 10 criterios fundamentales de consistencia.
"""

import re
from pathlib import Path
from decimal import Decimal
from django.core.management.base import BaseCommand, CommandError
from apps.catalogo.models import Producto


class Command(BaseCommand):
    help = "Audita la integridad de los 72 productos públicos de EduCompra contra CATALOGO_CURADO_FASE_3.md."

    def handle(self, *args, **options):
        catalogo_path = Path("CATALOGO_CURADO_FASE_3.md")
        if not catalogo_path.exists():
            raise CommandError("No se encontró el archivo canónico CATALOGO_CURADO_FASE_3.md.")

        text = catalogo_path.read_text(encoding="utf-8")

        # Extraer tabla de sección 3 para auditoría de advertencias
        table_rows = re.findall(
            r"\|\s*\d+\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|",
            text
        )
        table_warnings = {r[0].strip(): ("Sí" in r[7] or "⚠️" in r[7]) for r in table_rows}

        # Extraer fichas individuales de productos
        pattern = r"#### \[\d+\] `([^`]+)` — ([^\n]+)\n(.*?)(?=\n#### \[\d+\] `|\Z)"
        matches = list(re.finditer(pattern, text, re.DOTALL))

        self.stdout.write("=" * 70)
        self.stdout.write("AUDITORÍA DE INTEGRIDAD CANÓNICA FASE 4B — 72 PRODUCTOS EDUCOMPRA")
        self.stdout.write("=" * 70)

        if len(matches) != 72:
            raise CommandError(f"Se esperaban 72 fichas en CATALOGO_CURADO_FASE_3.md, encontradas {len(matches)}.")

        coincidencias = 0
        discrepancias = []

        for m in matches:
            sku_prov_header = m.group(1).strip()
            nombre_header = m.group(2).strip()
            body = m.group(3)

            sku_humm_m = re.search(r"-\s*\*\*SKU Proveedor:\*\*\s*`([^`]+)`\s*\|\s*\*\*SKU Humm:\*\*\s*`([^`]+)`", body)
            nom_m = re.search(r"-\s*\*\*Nombre Comercial Humm:\*\*\s*\*\*([^\*]+)\*\*", body)
            cat_m = re.search(r"-\s*\*\*Categoría:\*\*\s*([^\n]+)", body)
            precio_m = re.search(r"-\s*\*\*Precio Referencial Sugerido:\*\*\s*\*\*\$([\d\.,]+)\s*CLP\*\*", body)
            unidad_m = re.search(r"-\s*\*\*Unidad de Medida:\*\*\s*`([^`]+)`", body)

            sku_prov = sku_humm_m.group(1).strip() if sku_humm_m else sku_prov_header
            sku_humm = sku_humm_m.group(2).strip() if sku_humm_m else f"HUMM-KEY-{sku_prov}"
            nom_doc = nom_m.group(1).strip() if nom_m else nombre_header
            cat_doc = cat_m.group(1).strip() if cat_m else ""
            precio_doc_raw = re.sub(r"[^\d]", "", precio_m.group(1)) if precio_m else ""
            unidad_doc = unidad_m.group(1).strip() if unidad_m else "unidad"
            adv_doc = table_warnings.get(sku_prov, False)

            p = Producto.objects.filter(sku_proveedor=sku_prov).first()
            if not p:
                discrepancias.append(f"[{sku_prov}] No existe en la base de datos.")
                continue

            errores_p = []

            # 1. SKU Proveedor
            if p.sku_proveedor != sku_prov:
                errores_p.append(f"sku_proveedor: BD={p.sku_proveedor} vs Doc={sku_prov}")

            # 2. SKU Humm (Nomenclatura HUMM-KEY-XXXX)
            if p.sku_humm != sku_humm:
                errores_p.append(f"sku_humm: BD={p.sku_humm} vs Doc={sku_humm}")

            # 3. Nombre Comercial
            if p.nombre_comercial != nom_doc:
                errores_p.append(f"nombre_comercial: BD=\"{p.nombre_comercial}\" vs Doc=\"{nom_doc}\"")

            # 4. Categoría
            if not p.categoria or p.categoria.nombre != cat_doc:
                errores_p.append(f"categoría: BD=\"{p.categoria.nombre if p.categoria else None}\" vs Doc=\"{cat_doc}\"")

            # 5. Precio Referencial Total CLP
            if precio_doc_raw:
                precio_doc = Decimal(precio_doc_raw)
                if abs(p.precio_sugerido_total_clp - precio_doc) > Decimal("1.00"):
                    errores_p.append(f"precio: BD={p.precio_sugerido_total_clp} vs Doc={precio_doc}")

            # 6. Unidad Comercial
            if p.unidad_compra != unidad_doc:
                errores_p.append(f"unidad_compra: BD=\"{p.unidad_compra}\" vs Doc=\"{unidad_doc}\"")

            # 7. Imagen Principal
            if not p.imagenes.exists():
                errores_p.append("sin imagen asociada en BD")

            # 8. Advertencia de Uso
            tiene_adv_bd = bool(p.advertencia_uso and p.advertencia_uso.strip())
            if adv_doc != tiene_adv_bd:
                errores_p.append(f"advertencia_uso: BD={tiene_adv_bd} vs Doc={adv_doc}")

            # 9. Slug
            if not p.slug or not p.slug.strip():
                errores_p.append("slug vacío en BD")

            # 10. Publicado
            if not p.publicado:
                errores_p.append("publicado != True")

            if errores_p:
                discrepancias.append(f"[{sku_prov}] " + "; ".join(errores_p))
            else:
                coincidencias += 1

        self.stdout.write(f"Resultado: {coincidencias} / 72 productos validados con coincidencia exacta.")

        if discrepancias:
            self.stdout.write(self.style.ERROR(f"\nSe detectaron {len(discrepancias)} discrepancias:"))
            for d in discrepancias:
                self.stdout.write(f"  • {d}")
            raise CommandError("La auditoría de integridad falló. Existen discrepancias entre BD y la fuente canónica.")

        self.stdout.write(self.style.SUCCESS("\n✔ AUDITORÍA EXITOSA: 72 / 72 coincidencias exactas en los 10 criterios."))
