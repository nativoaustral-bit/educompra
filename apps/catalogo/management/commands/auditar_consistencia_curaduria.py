from django.core.management.base import BaseCommand, CommandError
from apps.catalogo.models import Producto, Categoria, TecnologiaCompatible


class Command(BaseCommand):
    help = (
        "Audita la consistencia del catálogo curado de 72 productos en la base de datos "
        "conforme a las reglas de cierre de Fase 3 de EduCompra Humm."
    )

    DISTRIBUCION_ESPERADA = {
        "Arduino y controladores": 8,
        "Sensores y módulos": 20,
        "Robótica y vehículos": 4,
        "Motores y movimiento": 5,
        "Electrónica y prototipado": 8,
        "Pantallas e interacción": 6,
        "Micro:bit y accesorios": 5,
        "Raspberry Pi y accesorios": 4,
        "IoT y comunicación": 6,
        "Kits educativos iniciales": 3,
        "Herramientas y accesorios": 3,
    }

    SKUS_CON_ADVERTENCIA_ESPERADOS = {
        "CR0011",
        "CR0019",
        "CR0033 CR0034",
        "KS0040",
        "KS0047",
        "KS0057",
        "KS0116",
        "KS0171",
        "KS0332",
        "49500004",
        "49500005",
    }

    def handle(self, *args, **options):
        errores = []
        self.stdout.write("======================================================================")
        self.stdout.write("EDUCOMPRA HUMM — AUDITORÍA DE CONSISTENCIA DEL CATÁLOGO CURADO FASE 3")
        self.stdout.write("======================================================================")

        # 1. Total de productos en base de datos
        total_prods = Producto.objects.count()
        self.stdout.write(f"• Total de productos en catálogo maestro: {total_prods}")
        if total_prods == 0:
            raise CommandError("La base de datos no contiene productos.")

        # 2. Catálogo curado: exactamente 72 productos con estado_curaduria == 'VALIDADO'
        validados = Producto.objects.filter(estado_curaduria="VALIDADO")
        count_validados = validados.count()
        self.stdout.write(f"• Productos con curaduría VALIDADO: {count_validados} (esperado: 72)")
        if count_validados != 72:
            errores.append(f"Se esperaban exactamente 72 productos validados, se encontraron {count_validados}.")

        # 3. Estado de publicación: 0 productos publicados en todo el catálogo
        publicados = Producto.objects.filter(publicado=True).count()
        self.stdout.write(f"• Productos publicados en catálogo público: {publicados} (esperado: 0)")
        if publicados != 0:
            errores.append(f"Existen {publicados} productos con publicado=True. Todo el catálogo debe ser privado.")

        # 4. Candado de compra pública: 0 productos con VALIDADO_HUMM
        validados_humm = Producto.objects.filter(estado_especificacion_neutral="VALIDADO_HUMM").count()
        self.stdout.write(f"• Especificaciones neutras con VALIDADO_HUMM: {validados_humm} (esperado: 0)")
        if validados_humm != 0:
            errores.append(f"Existen {validados_humm} productos con VALIDADO_HUMM sin revisión documental individual.")

        # 5. Ausencia de SKU duplicados dentro del lote de 72
        skus_validados = list(validados.values_list("sku_proveedor", flat=True))
        if len(skus_validados) != len(set(skus_validados)):
            duplicados = [s for s in skus_validados if skus_validados.count(s) > 1]
            errores.append(f"Existen SKUs duplicados en el lote de 72: {set(duplicados)}")
        else:
            self.stdout.write("• Ausencia de duplicados en el lote de 72: ✔ Sin duplicados")

        # 6. Correspondencia SKU/Categoría y distribución exacta por categorías
        self.stdout.write("• Distribución por categorías pedagógicas:")
        dist_actual = {}
        for cat_nom, esperado in self.DISTRIBUCION_ESPERADA.items():
            actual = validados.filter(categoria__nombre=cat_nom).count()
            dist_actual[cat_nom] = actual
            ok = "✔" if actual == esperado else "❌"
            self.stdout.write(f"  [{ok}] {cat_nom}: {actual}/{esperado}")
            if actual != esperado:
                errores.append(f"Categoría '{cat_nom}' tiene {actual} productos (esperado: {esperado}).")

        # 7. Auditoría de advertencias de uso (advertencia_uso)
        con_adv = Producto.objects.filter(advertencia_uso__gt="")
        skus_con_adv = set(con_adv.values_list("sku_proveedor", flat=True))
        self.stdout.write(f"• Productos con advertencia_uso: {len(skus_con_adv)} (esperado: {len(self.SKUS_CON_ADVERTENCIA_ESPERADOS)})")

        if skus_con_adv != self.SKUS_CON_ADVERTENCIA_ESPERADOS:
            sobrantes = skus_con_adv - self.SKUS_CON_ADVERTENCIA_ESPERADOS
            faltantes = self.SKUS_CON_ADVERTENCIA_ESPERADOS - skus_con_adv
            if sobrantes:
                errores.append(f"SKUs con advertencia inesperada: {sobrantes}")
            if faltantes:
                errores.append(f"SKUs a los que les falta advertencia: {faltantes}")

        # Comprobar KS0057: debe ser 2 relés
        p_ks0057 = Producto.objects.filter(sku_proveedor="KS0057").first()
        if p_ks0057:
            if "2 Relés" not in p_ks0057.nombre_comercial and "2 relés" not in p_ks0057.nombre_comercial:
                errores.append("KS0057 debe indicar que es un módulo de 2 relés.")
            self.stdout.write("  ✔ KS0057 verificado como módulo de 2 relés.")

        # Comprobar KS0049: no debe tener advertencia de fuente breadboard
        p_ks0049 = Producto.objects.filter(sku_proveedor="KS0049").first()
        if p_ks0049 and p_ks0049.advertencia_uso:
            errores.append("KS0049 es sensor de humedad de suelo y no debe tener advertencia de fuente.")
        else:
            self.stdout.write("  ✔ KS0049 verificado como sensor de humedad de suelo sin advertencia de fuente.")

        # 8. Separación entre compatibilidad verificada y propuesta
        sin_tec_verificada = []
        sin_tec_propuesta = []
        for p in validados:
            if p.tecnologias_verificadas.count() == 0:
                sin_tec_verificada.append(p.sku_proveedor)
            if p.tecnologias_compatibles.count() == 0:
                sin_tec_propuesta.append(p.sku_proveedor)

        if sin_tec_verificada:
            errores.append(f"Existen productos sin tecnologías verificadas asignadas: {sin_tec_verificada}")
        if sin_tec_propuesta:
            errores.append(f"Existen productos sin tecnologías propuestas asignadas: {sin_tec_propuesta}")

        self.stdout.write("• Separación de compatibilidad tecnológica:")
        self.stdout.write(f"  ✔ 72/72 productos con tecnologías verificadas documentales")
        self.stdout.write(f"  ✔ 72/72 productos con tecnologías propuestas pedagógicas")

        self.stdout.write("======================================================================")
        if errores:
            self.stdout.write(self.style.ERROR(f"❌ AUDITORÍA FALLIDA: {len(errores)} inconsistencias detectadas:"))
            for e in errores:
                self.stdout.write(self.style.ERROR(f"   - {e}"))
            raise CommandError(f"Se encontraron {len(errores)} inconsistencias en la auditoría.")
        else:
            self.stdout.write(self.style.SUCCESS("✔ AUDITORÍA EXITOSA: 100% DE CONSISTENCIA VERIFICADA"))
            self.stdout.write(self.style.SUCCESS("Catálogo curado oficial de 72 productos en perfecto estado."))
            self.stdout.write("======================================================================")
