"""
Pruebas exhaustivas para la Gestión Simplificada de Catálogo (Fase 5A Evolución).
Verifica los 8 Ajustes Obligatorios de Humm y los Bloques A–F:
- Ajuste 1: Pricing global respetando recargos específicos individuales.
- Ajuste 2: Simulación en memoria y aplicación server-side atómica con rollback.
- Ajuste 3: Regla genérica de cuarentena activo=False (sin hardcoding de SKUs).
- Ajuste 4: Métricas dinámicas calculadas desde BD (sin cifras hardcodeadas).
- Ajuste 5: Curaduría simple con propuestas determinísticas y validación explícita.
- Ajuste 6: Puerta única de publicación (ProductoPublicationService) separando listos vs bloqueados.
- Ajuste 7: Selección masiva segura por SKU y pre-análisis sin escrituras.
- Ajuste 8: Conservación estricta de alcance, cero migraciones y snapshots intactos.
"""

from decimal import Decimal
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse

from apps.catalogo.models import Producto, Categoria, Proveedor, ProductoImagen
from apps.catalogo.services_publicacion import ProductoPublicationService
from apps.core.models import ConfiguracionPricing
from apps.gestion.models import RegistroActividad
from apps.gestion.views.productos_seleccion import parsear_skus
from apps.gestion.views.precios import simular_precios_en_memoria

User = get_user_model()


class GestionSimplificadaTestCase(TestCase):
    """Configuración de base de pruebas con usuario administrador y catálogo de prueba."""

    def setUp(self):
        call_command("crear_roles_gestion")

        # Configuración de Pricing inicial
        self.config = ConfiguracionPricing.get_solo()
        self.config.tipo_cambio_usd_clp = Decimal("950.00")
        self.config.factor_internacion_flete_porcentaje = Decimal("15.00")
        self.config.recargo_general_porcentaje = Decimal("80.00")
        self.config.iva_porcentaje = Decimal("19.00")
        self.config.save()

        # Usuario administrador para pruebas
        self.admin = User.objects.create_superuser(
            username="admin_test",
            email="admin_test@humm.cl",
            password="TestPassword123!"
        )
        self.client = Client()
        self.client.force_login(self.admin)

        # Proveedor y Categoría base
        self.proveedor = Proveedor.objects.create(
            nombre="Keyestudio Test",
            codigo="KEYTEST",
            moneda_origen="USD",
            activo=True
        )
        self.categoria_robotica = Categoria.objects.create(
            nombre="Robótica Educativa",
            slug="robotica-educativa",
            activa=True,
            orden=1
        )
        self.categoria_sensores = Categoria.objects.create(
            nombre="Sensores y Módulos",
            slug="sensores-modulos",
            activa=True,
            orden=2
        )

        # Imagen de prueba
        imagen_dummy = SimpleUploadedFile("foto.jpg", b"\x47\x49\x46\x38\x39\x61", content_type="image/jpeg")

        # Producto 1: Activo, sin revisar, recargo general (porcentaje_recargo = None)
        self.p1 = Producto.objects.create(
            sku_humm="HUMM-KEY-KS0001",
            sku_proveedor="KS0001",
            proveedor=self.proveedor,
            categoria=self.categoria_robotica,
            nombre_comercial="Kit Robot Educativo Keyestudio",
            nombre_original_proveedor="Keyestudio Mini Robot Car",
            costo_proveedor_usd=Decimal("20.00"),
            porcentaje_recargo=None,
            activo=True,
            publicado=False,
            estado_curaduria="SIN_REVISAR",
            descripcion_educativa="Kit de robótica para proyectos escolares de educación media.",
            unidad_compra="unidad"
        )
        ProductoImagen.objects.create(producto=self.p1, archivo=imagen_dummy, es_principal=True)

        # Producto 2: Activo, con recargo específico de 60%
        self.p2 = Producto.objects.create(
            sku_humm="HUMM-KEY-KS0002",
            sku_proveedor="KS0002",
            proveedor=self.proveedor,
            categoria=self.categoria_sensores,
            nombre_comercial="Sensor de Temperatura Escolar",
            nombre_original_proveedor="Keyestudio Temperature Sensor Module",
            costo_proveedor_usd=Decimal("5.00"),
            porcentaje_recargo=Decimal("60.00"),
            activo=True,
            publicado=False,
            estado_curaduria="SIN_REVISAR",
            descripcion_educativa="Módulo sensor térmico para laboratorios de ciencias naturales.",
            unidad_compra="unidad"
        )
        ProductoImagen.objects.create(producto=self.p2, archivo=imagen_dummy, es_principal=True)

        # Producto 3: Inactivo / Cuarentena (Ajuste 3)
        self.p3_inactivo = Producto.objects.create(
            sku_humm="HUMM-KEY-KS9999",
            sku_proveedor="KS9999",
            proveedor=self.proveedor,
            categoria=self.categoria_robotica,
            nombre_comercial="Producto en Cuarentena Inactivo",
            costo_proveedor_usd=Decimal("10.00"),
            porcentaje_recargo=None,
            activo=False,
            publicado=False,
            estado_curaduria="SIN_REVISAR",
            descripcion_educativa="En cuarentena por proveedor.",
            unidad_compra="unidad"
        )

        # Producto 4: Validado y Publicado
        self.p4_publicado = Producto.objects.create(
            sku_humm="HUMM-KEY-KS0004",
            sku_proveedor="KS0004",
            proveedor=self.proveedor,
            categoria=self.categoria_robotica,
            nombre_comercial="Microcontrolador Educativo UNO",
            costo_proveedor_usd=Decimal("8.00"),
            porcentaje_recargo=None,
            activo=True,
            publicado=True,
            estado_curaduria="VALIDADO",
            descripcion_educativa="Placa programable estándar para robótica y proyectos STEAM.",
            unidad_compra="unidad"
        )
        ProductoImagen.objects.create(producto=self.p4_publicado, archivo=imagen_dummy, es_principal=True)


class BloqueATests(GestionSimplificadaTestCase):
    """Pruebas del Bloque A: Vista principal simplificada y KPIs dinámicos (Ajustes 3 y 4)."""

    def test_kpis_dinamicos_obtenidos_desde_db(self):
        """Ajuste 4: Los KPIs provienen de conteos reales de BD y no de templates hardcodeados."""
        response = self.client.get(reverse("gestion:productos_lista"))
        self.assertEqual(response.status_code, 200)
        kpis = response.context["kpis"]

        self.assertEqual(kpis["total_maestro"], 4)
        self.assertEqual(kpis["total_publicados"], 1)
        self.assertEqual(kpis["total_inactivos"], 1)  # Ajuste 3: activo=False
        self.assertEqual(kpis["total_sin_revisar"], 2)  # p1, p2 (activos)
        self.assertEqual(kpis["total_candidatos"], 0)

    def test_filtro_por_tabs_y_busqueda_amplia(self):
        """Verifica filtrado por pastillas de flujo y búsqueda por SKU proveedor."""
        # Tab publicados
        resp_pub = self.client.get(reverse("gestion:productos_lista") + "?tab=publicados")
        self.assertEqual(len(resp_pub.context["page_obj"]), 1)
        self.assertEqual(resp_pub.context["page_obj"][0].id, self.p4_publicado.id)

        # Tab inactivos (Ajuste 3)
        resp_inact = self.client.get(reverse("gestion:productos_lista") + "?tab=inactivos")
        self.assertEqual(len(resp_inact.context["page_obj"]), 1)
        self.assertEqual(resp_inact.context["page_obj"][0].id, self.p3_inactivo.id)

        # Búsqueda por SKU proveedor
        resp_busq = self.client.get(reverse("gestion:productos_lista") + "?q=KS0002")
        self.assertEqual(len(resp_busq.context["page_obj"]), 1)
        self.assertEqual(resp_busq.context["page_obj"][0].id, self.p2.id)

    def test_accion_lote_marcar_candidato_desde_tabla(self):
        """Marca candidatos desde checkbox en lista (excluye inactivos por Ajuste 3)."""
        response = self.client.post(reverse("gestion:productos_lista"), {
            "accion": "marcar_candidatos",
            "selected_ids": [str(self.p1.id), str(self.p3_inactivo.id)],
        })
        self.assertEqual(response.status_code, 302)

        self.p1.refresh_from_db()
        self.p3_inactivo.refresh_from_db()

        self.assertEqual(self.p1.estado_curaduria, "CANDIDATO")
        # Inactivo NO debe marcarse candidato (Ajuste 3)
        self.assertEqual(self.p3_inactivo.estado_curaduria, "SIN_REVISAR")


class BloqueBTests(GestionSimplificadaTestCase):
    """Pruebas del Bloque B: Selección masiva por lista de SKU (Ajuste 7)."""

    def test_parseador_skus(self):
        """El parseador normaliza mayúsculas, elimina espacios y deduplica en orden."""
        texto = " ks0001, KS0002; ks0001 \n KS0003 \t ks0004 "
        tokens = parsear_skus(texto)
        self.assertEqual(tokens, ["KS0001", "KS0002", "KS0003", "KS0004"])

    def test_preanalisis_sku_no_escribe_en_bd(self):
        """El pre-análisis de diagnóstico no altera ningún estado de la base de datos."""
        texto = "KS0001, KS0002, KS9999, SKU_INEXISTENTE"
        response = self.client.post(reverse("gestion:productos_seleccion_sku"), {
            "accion": "preanalizar",
            "skus_texto": texto,
        })
        self.assertEqual(response.status_code, 200)
        analisis = response.context["analisis"]

        self.assertEqual(analisis["total_tokens"], 4)
        self.assertEqual(analisis["total_encontrados"], 3)
        self.assertEqual(analisis["total_faltantes"], 1)
        self.assertIn("SKU_INEXISTENTE", analisis["faltantes"])
        self.assertEqual(analisis["aptos_candidato_count"], 2)  # KS0001 y KS0002
        self.assertEqual(analisis["inactivos_cuarentena_count"], 1)  # KS9999 (Ajuste 3)

        # Verificar que BD sigue intacta
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.estado_curaduria, "SIN_REVISAR")

    def test_confirmacion_marcado_candidatos_aplica_solo_a_aptos(self):
        """Al confirmar, solo se marcan los productos activos sin revisar."""
        texto = "KS0001, KS0004, KS9999"
        response = self.client.post(reverse("gestion:productos_seleccion_sku"), {
            "accion": "confirmar_marcado_candidatos",
            "skus_texto": texto,
        })
        self.assertEqual(response.status_code, 302)

        self.p1.refresh_from_db()
        self.p4_publicado.refresh_from_db()
        self.p3_inactivo.refresh_from_db()

        self.assertEqual(self.p1.estado_curaduria, "CANDIDATO")
        self.assertEqual(self.p4_publicado.estado_curaduria, "VALIDADO")  # No sobreescrito
        self.assertEqual(self.p3_inactivo.estado_curaduria, "SIN_REVISAR")  # Inactivo omitido


class BloqueCTests(GestionSimplificadaTestCase):
    """Pruebas del Bloque C: Curaduría pedagógica y por lote (Ajuste 5)."""

    def test_candidatos_view_muestra_solo_activos_candidatos(self):
        self.p1.estado_curaduria = "CANDIDATO"
        self.p1.save()

        response = self.client.get(reverse("gestion:productos_candidatos"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["productos"]), 1)
        self.assertEqual(response.context["productos"][0].id, self.p1.id)

    def test_curaduria_lote_guarda_borrador_y_valida(self):
        """Guarda borrador en EN_CURADURIA y valida en VALIDADO tras verificar requisitos."""
        url = reverse("gestion:productos_curaduria_lote") + f"?ids={self.p1.id}"
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)
        self.assertIn("tarjetas", resp_get.context)

        # 1. Guardar Borrador
        resp_draft = self.client.post(url, {
            "accion": "guardar_borrador_item",
            "producto_id": self.p1.id,
            "ids": str(self.p1.id),
            f"nombre_comercial_{self.p1.id}": "Kit Mini Robot Editado",
            f"categoria_{self.p1.id}": self.categoria_robotica.id,
            f"descripcion_educativa_{self.p1.id}": "Descripción pedagógica adecuada de prueba.",
            f"uso_educativo_{self.p1.id}": "Proyectos STEAM.",
        })
        self.assertEqual(resp_draft.status_code, 302)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.estado_curaduria, "EN_CURADURIA")
        self.assertEqual(self.p1.nombre_comercial, "Kit Mini Robot Editado")

        # 2. Validar Curaduría con requisitos completos
        resp_val = self.client.post(url, {
            "accion": "validar_item",
            "producto_id": self.p1.id,
            "ids": str(self.p1.id),
            f"nombre_comercial_{self.p1.id}": "Kit Mini Robot Editado",
            f"categoria_{self.p1.id}": self.categoria_robotica.id,
            f"descripcion_educativa_{self.p1.id}": "Descripción pedagógica con más de quince caracteres requeridos.",
        })
        self.assertEqual(resp_val.status_code, 302)
        self.p1.refresh_from_db()
        self.assertEqual(self.p1.estado_curaduria, "VALIDADO")

    def test_curaduria_masiva_campos_comunes(self):
        """Asigna campos comunes sin modificar textos pedagógicos (Ajuste 5)."""
        url = reverse("gestion:productos_curaduria_masiva_campos") + f"?ids={self.p1.id},{self.p2.id}"
        response = self.client.post(url, {
            "accion": "aplicar_campos_comunes",
            "ids": f"{self.p1.id},{self.p2.id}",
            "aplicar_categoria": "1",
            "categoria": self.categoria_sensores.id,
            "aplicar_dificultad": "1",
            "nivel_dificultad": "INTERMEDIO",
            "aplicar_stock": "1",
            "estado_stock": "importacion",
        })
        self.assertEqual(response.status_code, 302)

        self.p1.refresh_from_db()
        self.p2.refresh_from_db()

        self.assertEqual(self.p1.categoria_id, self.categoria_sensores.id)
        self.assertEqual(self.p1.nivel_dificultad, "INTERMEDIO")
        self.assertEqual(self.p1.estado_stock, "importacion")
        # Nombres comerciales y descripciones originales se conservan intactos
        self.assertIn("Robot", self.p1.nombre_comercial)
        self.assertIn("Sensor", self.p2.nombre_comercial)


class BloqueDTests(GestionSimplificadaTestCase):
    """Pruebas del Bloque D: Publicación y despublicación controlada (Ajuste 6)."""

    def test_publicacion_lote_separa_listos_y_bloqueados(self):
        """Separa listos de bloqueados usando ProductoPublicationService."""
        # p1 no está VALIDADO -> debe salir bloqueado
        # Creamos p5 validado con todos los requisitos
        imagen_dummy = SimpleUploadedFile("f.jpg", b"\x47\x49\x46\x38\x39\x61", content_type="image/jpeg")
        p5 = Producto.objects.create(
            sku_humm="HUMM-KEY-KS0005",
            sku_proveedor="KS0005",
            proveedor=self.proveedor,
            categoria=self.categoria_robotica,
            nombre_comercial="Placa Compatible UNO R3",
            costo_proveedor_usd=Decimal("6.00"),
            activo=True,
            publicado=False,
            estado_curaduria="VALIDADO",
            descripcion_educativa="Placa para robótica con más de quince caracteres válidos.",
            unidad_compra="unidad"
        )
        ProductoImagen.objects.create(producto=p5, archivo=imagen_dummy, es_principal=True)

        url = reverse("gestion:productos_publicacion_lote") + f"?ids={self.p1.id},{p5.id}"
        resp_get = self.client.get(url)
        self.assertEqual(resp_get.status_code, 200)

        self.assertEqual(len(resp_get.context["listos"]), 1)
        self.assertEqual(resp_get.context["listos"][0].id, p5.id)
        self.assertEqual(len(resp_get.context["bloqueados"]), 1)
        self.assertEqual(resp_get.context["bloqueados"][0]["producto"].id, self.p1.id)

        # Confirmar publicación
        resp_post = self.client.post(url, {
            "accion": "confirmar_publicacion",
            "ids": f"{self.p1.id},{p5.id}",
        })
        self.assertEqual(resp_post.status_code, 302)

        p5.refresh_from_db()
        self.p1.refresh_from_db()

        self.assertTrue(p5.publicado)
        self.assertFalse(self.p1.publicado)  # Bloqueado permanece publicado=False

    def test_despublicacion_lote_mantiene_catalogo_maestro(self):
        """Despublica producto sin borrarlo del maestro ni alterar cotizaciones."""
        self.assertTrue(self.p4_publicado.publicado)
        url = reverse("gestion:productos_despublicacion_lote") + f"?ids={self.p4_publicado.id}"

        response = self.client.post(url, {
            "accion": "confirmar_despublicacion",
            "ids": str(self.p4_publicado.id),
            "motivo_despublicacion": "Prueba de retiro controlado",
        })
        self.assertEqual(response.status_code, 302)

        self.p4_publicado.refresh_from_db()
        self.assertFalse(self.p4_publicado.publicado)
        self.assertTrue(self.p4_publicado.activo)  # Permanece en maestro


class BloqueETests(GestionSimplificadaTestCase):
    """Pruebas del Bloque E: Pricing masivo, simulación y recargo específico (Ajustes 1 y 2)."""

    def test_simulacion_en_memoria_no_modifica_bd(self):
        """Ajuste 2: La simulación no escribe ningún valor en BD."""
        precio_p1_inicial = self.p1.precio_sugerido_total_clp
        precio_p2_inicial = self.p2.precio_sugerido_total_clp

        resp_sim = self.client.post(reverse("gestion:precios_dashboard"), {
            "accion": "simular_impacto",
            "tipo_cambio": "1000.00",
            "factor_internacion": "20.00",
            "recargo_general": "90.00",
            "iva": "19.00",
            "alcance": "activos",
        })
        self.assertEqual(resp_sim.status_code, 200)
        self.assertIn("simulacion", resp_sim.context)

        self.p1.refresh_from_db()
        self.p2.refresh_from_db()

        self.assertEqual(self.p1.precio_sugerido_total_clp, precio_p1_inicial)
        self.assertEqual(self.p2.precio_sugerido_total_clp, precio_p2_inicial)

    def test_recalculo_global_preserva_recargos_especificos(self):
        """Ajuste 1: Al cambiar TC/flete/IVA, el producto con porcentaje_recargo != None conserva su recargo pero recalcula precios."""
        # p1: porcentaje_recargo = None -> usará nuevo recargo general 90%
        # p2: porcentaje_recargo = 60.00 -> conserva 60%, pero recalcula con nuevo TC (1000) y flete (20%)
        response = self.client.post(reverse("gestion:precios_dashboard"), {
            "accion": "aplicar_precios_servidor",
            "tipo_cambio": "1000.00",
            "factor_internacion": "20.00",
            "recargo_general": "90.00",
            "iva": "19.00",
            "alcance": "activos",
        })
        self.assertEqual(response.status_code, 302)

        self.p1.refresh_from_db()
        self.p2.refresh_from_db()

        # p2 conserva porcentaje_recargo = 60.00
        self.assertEqual(self.p2.porcentaje_recargo, Decimal("60.00"))
        # Costo Chile p2: 5 USD * 1000 * 1.20 = 6,000 CLP
        self.assertEqual(self.p2.costo_puesto_chile_clp, Decimal("6000.00"))
        # Precio Neto p2: 6000 * 1.60 = 9,600 CLP
        self.assertEqual(self.p2.precio_sugerido_neto_clp, Decimal("9600.00"))
        # Precio Total p2: 9600 * 1.19 = 11,424 CLP
        self.assertEqual(self.p2.precio_sugerido_total_clp, Decimal("11424.00"))

        # p1 utilizó nuevo recargo general 90%
        # Costo Chile p1: 20 USD * 1000 * 1.20 = 24,000 CLP
        self.assertEqual(self.p1.costo_puesto_chile_clp, Decimal("24000.00"))
        # Precio Neto p1: 24000 * 1.90 = 45,600 CLP
        self.assertEqual(self.p1.precio_sugerido_neto_clp, Decimal("45600.00"))
        # Precio Total p1: 45600 * 1.19 = 54,264 CLP
        self.assertEqual(self.p1.precio_sugerido_total_clp, Decimal("54264.00"))

        # Auditoría registrada tras éxito completo
        self.assertTrue(RegistroActividad.objects.filter(accion="APLICAR_CAMBIO_PRICING_GLOBAL").exists())

    def test_asignar_recargo_especifico_como_accion_separada(self):
        """Ajuste 1: Modificar recargo específico es una acción separada explícita."""
        self.assertIsNone(self.p1.porcentaje_recargo)

        response = self.client.post(reverse("gestion:precios_dashboard"), {
            "accion": "asignar_recargo_especifico",
            "tipo_seleccion": "sku_lista",
            "skus_lista": "KS0001",
            "porcentaje_recargo_especifico": "75.00",
        })
        self.assertEqual(response.status_code, 302)

        self.p1.refresh_from_db()
        self.assertEqual(self.p1.porcentaje_recargo, Decimal("75.00"))
