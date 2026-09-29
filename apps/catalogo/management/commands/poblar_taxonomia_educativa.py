from django.core.management.base import BaseCommand
from apps.catalogo.models import Categoria, TecnologiaCompatible


class Command(BaseCommand):
    help = "Crea o actualiza la taxonomía pedagógica de 11 categorías docentes y las tecnologías compatibles controladas."

    def handle(self, *args, **options):
        self.stdout.write("=" * 70)
        self.stdout.write("EDUCOMPRA HUMM — SEMBRADOR DE TAXONOMÍA PEDAGÓGICA Y TECNOLOGÍAS")
        self.stdout.write("=" * 70)

        # 1. Categorías Docentes Aprobadas (11 principales + Sin clasificar interna)
        categorias = [
            {
                "nombre": "Arduino y controladores",
                "slug": "arduino-controladores",
                "orden": 10,
                "descripcion": "Placas de procesamiento base (UNO, Nano, Mega, ESP32) para aprender programación y robótica.",
            },
            {
                "nombre": "Sensores y módulos",
                "slug": "sensores-modulos",
                "orden": 20,
                "descripcion": "Dispositivos para medir variables físicas del entorno: luz, temperatura, humedad, distancia, gas y sonido.",
            },
            {
                "nombre": "Robótica y vehículos",
                "slug": "robotica-vehiculos",
                "orden": 30,
                "descripcion": "Kits de robótica móvil, chasis de vehículos, brazos robóticos y sistemas mecatrónicos escolares.",
            },
            {
                "nombre": "Motores y movimiento",
                "slug": "motores-movimiento",
                "orden": 40,
                "descripcion": "Servomotores, motores DC, motores paso a paso y controladores de potencia (drivers) para proyectos.",
            },
            {
                "nombre": "Electrónica y prototipado",
                "slug": "electronica-prototipado",
                "orden": 50,
                "descripcion": "Protoboards, cables jumper, LEDs, resistencias, pulsadores, zumbadores y componentes de circuito.",
            },
            {
                "nombre": "Pantallas e interacción",
                "slug": "pantallas-interaccion",
                "orden": 60,
                "descripcion": "Displays LCD, pantallas OLED, matrices LED y módulos de entrada (joysticks, teclados numéricos).",
            },
            {
                "nombre": "Micro:bit y accesorios",
                "slug": "microbit",
                "orden": 70,
                "descripcion": "Placas de expansión, shields para sensores y kits temáticos adaptados a la plataforma micro:bit.",
            },
            {
                "nombre": "Raspberry Pi y accesorios",
                "slug": "raspberry-pi",
                "orden": 80,
                "descripcion": "Shields GPIO, placas adaptadoras, cámaras y periféricos para computación física y Linux.",
            },
            {
                "nombre": "IoT y comunicación",
                "slug": "iot-comunicacion",
                "orden": 90,
                "descripcion": "Módulos de conectividad inalámbrica Wi-Fi, Bluetooth, RFID y telemetría para proyectos conectados.",
            },
            {
                "nombre": "Kits educativos iniciales",
                "slug": "kits-educativos",
                "orden": 100,
                "descripcion": "Sets completos y estructurados con guías paso a paso para inicio de talleres y academias STEM.",
            },
            {
                "nombre": "Herramientas y accesorios",
                "slug": "herramientas-accesorios",
                "orden": 110,
                "descripcion": "Fuentes de alimentación, portapilas, cables de conexión USB y herramientas para taller escolar.",
            },
            {
                "nombre": "Sin clasificar",
                "slug": "sin-clasificar",
                "orden": 999,
                "descripcion": "Categoría interna provisional para productos del catálogo maestro pendientes de curaduría pedagógica.",
            },
        ]

        cat_creadas = 0
        cat_actualizadas = 0
        for data in categorias:
            cat, created = Categoria.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "nombre": data["nombre"],
                    "orden": data["orden"],
                    "descripcion": data["descripcion"],
                    "activa": True,
                },
            )
            if created:
                cat_creadas += 1
                self.stdout.write(f"  + Creada categoría: {cat.nombre} (orden {cat.orden})")
            else:
                cat_actualizadas += 1
                self.stdout.write(f"  * Actualizada categoría: {cat.nombre} (orden {cat.orden})")

        self.stdout.write(self.style.SUCCESS(f"✔ Categorías procesadas: {cat_creadas} creadas, {cat_actualizadas} actualizadas.\n"))

        # 2. Tecnologías Compatibles Controladas
        tecnologias = [
            {
                "nombre": "Arduino",
                "slug": "arduino",
                "orden": 10,
                "descripcion": "Plataforma de hardware libre y microcontroladores basados en C/C++ (UNO, Nano, Mega).",
            },
            {
                "nombre": "ESP32",
                "slug": "esp32",
                "orden": 20,
                "descripcion": "Microcontroladores con conectividad Wi-Fi y Bluetooth de alto rendimiento.",
            },
            {
                "nombre": "micro:bit",
                "slug": "microbit",
                "orden": 30,
                "descripcion": "Placa educativa BBC micro:bit diseñada para programación por bloques y MakeCode.",
            },
            {
                "nombre": "Raspberry Pi",
                "slug": "raspberry-pi",
                "orden": 40,
                "descripcion": "Microordenadores de placa reducida y módulos de cómputo para Python y Linux escolar.",
            },
            {
                "nombre": "Otros",
                "slug": "otros",
                "orden": 50,
                "descripcion": "Otras plataformas electrónicas o componentes pasivos de uso transversal y universal.",
            },
        ]

        tec_creadas = 0
        tec_actualizadas = 0
        for data in tecnologias:
            tec, created = TecnologiaCompatible.objects.update_or_create(
                slug=data["slug"],
                defaults={
                    "nombre": data["nombre"],
                    "orden": data["orden"],
                    "descripcion": data["descripcion"],
                    "activa": True,
                },
            )
            if created:
                tec_creadas += 1
                self.stdout.write(f"  + Creada tecnología: {tec.nombre} (orden {tec.orden})")
            else:
                tec_actualizadas += 1
                self.stdout.write(f"  * Actualizada tecnología: {tec.nombre} (orden {tec.orden})")

        self.stdout.write(self.style.SUCCESS(f"✔ Tecnologías procesadas: {tec_creadas} creadas, {tec_actualizadas} actualizadas."))
        self.stdout.write("=" * 70)
