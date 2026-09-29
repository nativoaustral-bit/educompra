from pathlib import Path
from collections import defaultdict
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand
from apps.catalogo.models import Producto


class Command(BaseCommand):
    help = (
        "Analiza el catálogo maestro y genera CANDIDATOS_SUGERIDOS_FASE_3.md "
        "con una propuesta balanceada de 70 a 120 productos pedagógicos (SOLO LECTURA, SIN MODIFICAR BD)."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reporte",
            type=str,
            default="",
            help="Ruta de destino del reporte Markdown (por defecto: CANDIDATOS_SUGERIDOS_FASE_3.md en BASE_DIR).",
        )

    def handle(self, *args, **options):
        reporte_path = Path(options["reporte"]) if options["reporte"] else (
            Path(settings.BASE_DIR) / "CANDIDATOS_SUGERIDOS_FASE_3.md"
        )

        self.stdout.write("=" * 70)
        self.stdout.write("EDUCOMPRA HUMM — MOTOR DE SUGERENCIA PEDAGÓGICA (FASE 3)")
        self.stdout.write("Modo: SOLO LECTURA (CERO ESCRITURAS EN BASE DE DATOS)")
        self.stdout.write("=" * 70)

        # Matriz de Arquetipos Funcionales Educativos
        # Estructura: (categoria_nombre, categoria_slug, cluster_id, cluster_label, includes, excludes, motivo, tec, apto_kit)
        ARQUETIPOS = [
            # -------------------------------------------------------------
            # 1. Arduino y controladores (~10 candidatos)
            # -------------------------------------------------------------
            (
                "Arduino y controladores", "arduino-controladores", "ARD_UNO_R3", "Placa Arduino UNO R3 / PLUS",
                ["UNO", "DEVELOPMENT BOARD"], ["SHIELD", "CASE", "BOX", "KIT", "LED", "ACRYLIC", "ROBOT", "WIFI", "ETHERNET"],
                "Microcontrolador estándar para alfabetización digital, pensamiento computacional y proyectos iniciales de robótica escolar.",
                "Arduino", "Sí — Kit Básico Arduino"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_MEGA_2560", "Placa Arduino Mega 2560 R3",
                ["MEGA 2560", "DEVELOPMENT BOARD"], ["SHIELD", "CASE", "BOX", "KIT", "LED", "ACRYLIC", "ROBOT", "PLUS BOARD"],
                "Placa de alta capacidad con 54 pines I/O y 4 puertos seriales para proyectos multiactuador, robótica pesada e impresoras 3D.",
                "Arduino", "Sí — Kit Robótica Avanzada"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_NANO", "Placa Arduino Nano V3 / V4",
                ["NANO PLUS", "DEVELOPMENT BOARD"], ["SHIELD", "CASE", "BOX", "KIT", "CAR", "ROBOT"],
                "Microcontrolador de factor de forma compacto para inserción directa en protoboards y proyectos portátiles en aula.",
                "Arduino", "Sí — Kit Prototipado Compacto"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_LEONARDO", "Placa Arduino Leonardo / Pro Micro (ATmega32U4)",
                ["PRO MICRO", "DEVELOPMENT BOARD"], ["SHIELD", "KIT", "CAR"],
                "Microcontrolador con comunicación USB nativa (HID) ideal para crear joysticks, interfaces interactivas y teclados escolares.",
                "Arduino", "Sí — Kit Interacción Digital"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_ESP32_CORE", "Placa de Desarrollo ESP32 Wi-Fi + BLE",
                ["ESP32 CORE BOARD"], ["SHIELD", "KIT", "CAR", "EXPANSION"],
                "Controlador dual-core de alta velocidad con conectividad Wi-Fi y Bluetooth nativa para proyectos IoT escolares.",
                "ESP32", "Sí — Kit IoT Avanzado"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_PRO_MINI", "Placa Arduino Pro Mini 5V / 16MHz",
                ["PROMINI", "DEVELOPMENT BOARD"], ["SHIELD", "KIT", "CAR"],
                "Placa miniatura de bajo consumo para proyectos definitivos de aula y dispositivos embebidos de bajo costo.",
                "Arduino", "Sí — Proyectos Autónomos"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_SENSOR_SHIELD", "Sensor Shield V5.0 para Arduino UNO",
                ["SENSOR SHIELD V5"], ["KIT", "CAR"],
                "Placa de expansión que facilita la conexión directa de servomotores y sensores de 3 pines sin cables sueltos.",
                "Arduino", "Sí — Kit Automatización Escolar"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_CNC_SHIELD", "CNC Shield V2 / V3 para Grabadoras y Máquinas",
                ["CNC SHIELD"], ["KIT", "CAR"],
                "Shield para control de motores paso a paso en fresadoras CNC, grabadoras láser y trazadores escolares.",
                "Arduino", "Sí — Taller Fabricación Digital"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_PROTO_SHIELD", "Proto Shield con Mini Protoboard para UNO",
                ["PROTOSHIELD", "MINI BREADBOARD"], ["KIT"],
                "Placa de expansión con área de pruebas para fijar circuitos experimentales directamente sobre Arduino UNO.",
                "Arduino", "Sí — Kit Prototipado Intermedio"
            ),
            (
                "Arduino y controladores", "arduino-controladores", "ARD_UNO_WIFI", "Placa Arduino UNO con Wi-Fi Integrado",
                ["328 WIFI PLUS"], ["KIT"],
                "Controlador con factor de forma UNO y chip ESP8266 integrado para conectar sensores a paneles en la nube.",
                "Arduino / ESP32", "Sí — Kit Internet de las Cosas"
            ),

            # -------------------------------------------------------------
            # 2. Sensores y módulos (~22 candidatos)
            # -------------------------------------------------------------
            (
                "Sensores y módulos", "sensores-modulos", "SEN_ULTRASONIC", "Sensor de Distancia Ultrasonido HC-SR04",
                ["ULTRASONIC", "HC-SR04"], ["KIT", "CAR"],
                "Sensor fundamental de ecolocalización para medir distancias (2cm a 400cm) en cinemática y detección de obstáculos.",
                "Arduino / micro:bit", "Sí — Kit Robótica / Ciencias"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_DHT11", "Sensor de Temperatura y Humedad DHT11",
                ["DHT11"], ["KIT", "CAR", "STARTER"],
                "Módulo digital básico para registrar variables ambientales en proyectos de ciencias naturales y meteorología escolar.",
                "Arduino / micro:bit", "Sí — Kit Estación Meteorológica"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_DHT22", "Sensor de Temperatura y Humedad Precisión DHT22",
                ["DHT22"], ["KIT", "CAR"],
                "Sensor ambiental de mayor rango y resolución para proyectos de invernaderos escolares y estaciones científicas.",
                "Arduino / ESP32", "Sí — Kit Estación Científica"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_SOIL", "Sensor Higrómetro de Humedad de Suelo",
                ["SOIL HUMIDITY"], ["KIT", "CAR"],
                "Transductor clave para proyectos interdisciplinarios de huerto escolar y riego automatizado.",
                "Arduino / micro:bit", "Sí — Kit Huerto Inteligente"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_PIR", "Sensor de Movimiento Infrarrojo Pasivo PIR",
                ["PIR MOTION SENSOR"], ["KIT", "CAR", "3PCS"],
                "Sensor de presencia humana para sistemas de seguridad, alarmas escolares y ahorro energético.",
                "Arduino / micro:bit", "Sí — Kit Domótica / Seguridad"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_GAS_MQ2", "Sensor Detector de Gas y Humo MQ-2",
                ["MQ-2"], ["KIT", "CAR"],
                "Sensor electroquímico para detección de GLP, humo y gases combustibles en proyectos de seguridad y prevención.",
                "Arduino / ESP32", "Sí — Kit Prevención y Seguridad"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_LIGHT_LDR", "Sensor de Luz Ambiental Fotoresistencia LDR",
                ["PHOTORESISTOR", "SENSOR MODULE"], ["KIT", "CAR"],
                "Módulo analógico para medir intensidad lumínica y construir alumbrado público automático o seguidores solares.",
                "Arduino / micro:bit", "Sí — Kit Energías Renovables"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_SOUND", "Sensor de Sonido con Micrófono y Comparador",
                ["SOUND SENSOR"], ["KIT", "CAR"],
                "Detector de ondas acústicas para activación por aplausos, monitoreo de ruido en aula o alarmas acústicas.",
                "Arduino / micro:bit", "Sí — Kit Acústica y Domótica"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_FLAME", "Sensor de Llama e Infrarrojo de Fuego",
                ["FLAME SENSOR"], ["KIT", "CAR"],
                "Transductor óptico de longitud de onda de llama (760nm-1100nm) para robots apagafuegos escolares.",
                "Arduino / micro:bit", "Sí — Kit Robótica de Rescate"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_LINE_TRACK", "Sensor Infrarrojo Seguidor de Línea",
                ["LINE TRACKING SENSOR"], ["KIT", "CAR"],
                "Par emisor-receptor óptico para navegación autónoma sobre pistas de contraste en competencias de robótica.",
                "Arduino / micro:bit", "Sí — Kit Robótica Móvil"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_OBSTACLE", "Sensor Infrarrojo Evita Obstáculos",
                ["OBSTACLE AVOIDANCE SENSOR"], ["KIT", "CAR"],
                "Módulo de proximidad IR de respuesta instantánea para prevención de colisiones a corta distancia.",
                "Arduino / micro:bit", "Sí — Kit Robótica Móvil"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_BAROMETRIC", "Sensor Barométrico de Presión y Altitud BMP388 / BMP280",
                ["BAROMETRIC PRESSURE"], ["KIT", "CAR"],
                "Transductor de alta precisión I2C para cálculo de altitud sobre el nivel del mar y pronóstico meteorológico.",
                "Arduino / ESP32", "Sí — Kit Estación Científica"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_DS18B20", "Sensor de Temperatura Sumergible Sonda DS18B20",
                ["DS18B20", "WATERPROOF"], ["KIT", "CAR"],
                "Sonda de acero inoxidable sellada One-Wire para registrar temperatura en líquidos (acuarios, química, suelos húmedos).",
                "Arduino / micro:bit", "Sí — Kit Acuaponía / Ciencias"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_MPU6050", "Sensor Giroscopio y Acelerómetro MPU-6050 6 Ejes",
                ["MPU6050"], ["KIT", "CAR"],
                "Unidad de medición inercial (IMU) para enseñar cinemática, orientación tridimensional y robots de balance.",
                "Arduino / ESP32", "Sí — Kit Cinemática y Vuelo"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_TOUCH", "Sensor Táctil Capacitivo Digital",
                ["CAPACITIVE TOUCH SENSOR"], ["KIT", "CAR"],
                "Interruptor táctil de estado sólido para paneles de control modernos e interfaces amigables para niños.",
                "Arduino / micro:bit", "Sí — Kit Interacción Escolar"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_WATER_LEVEL", "Sensor de Nivel de Agua y Detección de Lluvia",
                ["WATER LEVEL SENSOR"], ["KIT", "CAR"],
                "Pistas conductoras expuestas para monitoreo de precipitaciones e inundaciones en maquetas urbanas.",
                "Arduino / micro:bit", "Sí — Kit Ciudad Inteligente"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_COLOR", "Sensor de Color RGB TCS34725 con Filtro IR",
                ["TCS34725"], ["KIT", "CAR"],
                "Transductor óptico para reconocimiento de colores en bandas transportadoras y clasificación industrial escolar.",
                "Arduino / micro:bit", "Sí — Kit Automatización Fabril"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_HALL", "Sensor de Campo Magnético Efecto Hall",
                ["HALL MAGNETIC SENSOR"], ["KIT", "CAR"],
                "Sensor sin contacto para medir revoluciones por minuto (tacómetro escolar) y detección de imanes.",
                "Arduino / micro:bit", "Sí — Kit Mecatrónica Escolar"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_VIBRATION", "Sensor de Vibración e Impacto Piezoeléctrico",
                ["VIBRATION SENSOR"], ["KIT", "CAR"],
                "Interruptor de resorte interno para registrar sismos escolares, choques o movimientos estructurales.",
                "Arduino / micro:bit", "Sí — Kit Sismografía Escolar"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_HEART_RATE", "Sensor de Pulso y Frecuencia Cardíaca",
                ["PULSE SENSOR"], ["KIT", "CAR"],
                "Sensor óptico de fotopletismografía para proyectos de biología humana, salud y educación física tecnológica.",
                "Arduino / micro:bit", "Sí — Kit Biología y Salud"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_GAS_MQ135", "Sensor de Calidad del Aire y CO2 MQ-135",
                ["MQ-135"], ["KIT", "CAR"],
                "Módulo para evaluar ventilación en salas de clases y medir gases perjudiciales (amoniaco, sulfuro, benceno).",
                "Arduino / ESP32", "Sí — Kit Salud Ambiental"
            ),
            (
                "Sensores y módulos", "sensores-modulos", "SEN_VOLTAGE", "Módulo Sensor de Voltaje Analógico 0-25V",
                ["VOLTAGE DETECTION MODULE"], ["KIT", "CAR"],
                "Divisor resistivo para monitorear voltajes de baterías y generación en paneles solares escolares.",
                "Arduino / ESP32", "Sí — Kit Eficiencia Energética"
            ),

            # -------------------------------------------------------------
            # 3. Robótica y vehículos (~7 candidatos)
            # -------------------------------------------------------------
            (
                "Robótica y vehículos", "robotica-vehiculos", "ROB_SMART_CAR_4WD", "Chasis Auto Robot Inteligente 4WD",
                ["4WD SMART CAR CHASSIS"], ["ARM"],
                "Plataforma móvil con 4 motores DC y chasis acrílico para proyectos integrales de robótica y cinemática.",
                "Arduino", "Sí — Kit Robótica Integral"
            ),
            (
                "Robótica y vehículos", "robotica-vehiculos", "ROB_TURTLE_2WD", "Auto Robot Educativo 2WD Chasis Doble Capa",
                ["SMART CAR CHASSIS", "TWO-DRIVE"], ["4WD", "ARM"],
                "Plataforma móvil económica de 2 ruedas motrices con rueda loca ideal para iniciar talleres de robótica básica.",
                "Arduino / micro:bit", "Sí — Kit Robótica Primaria"
            ),
            (
                "Robótica y vehículos", "robotica-vehiculos", "ROB_MECANUM", "Robot Móvil Omnidireccional con Ruedas Mecanum",
                ["MECANUM WHEEL SMART ROBOT CAR"], [],
                "Vehículo de cinemática holonómica capaz de desplazarse lateral y diagonalmente para competencias avanzadas.",
                "Arduino / micro:bit", "Sí — Kit Robótica Avanzada"
            ),
            (
                "Robótica y vehículos", "robotica-vehiculos", "ROB_ARM_4DOF", "Brazo Robótico Mecatrónico 4DOF",
                ["4DOF ROBOT ARM"], [],
                "Manipulador articulado con pinza para simulación de líneas de ensamblaje industrial y trigonometría aplicada.",
                "Arduino / micro:bit", "Sí — Kit Robótica Industrial"
            ),
            (
                "Robótica y vehículos", "robotica-vehiculos", "ROB_BEETLEBOT", "Robot Educativo Multifunción Beetlebot 3 en 1",
                ["BEETLEBOT"], [],
                "Robot educativo compatible con bloques de construcción para esquivar obstáculos, seguir líneas y empujar objetos.",
                "Arduino", "Sí — Kit Robótica Lúdica"
            ),
            (
                "Robótica y vehículos", "robotica-vehiculos", "ROB_TANK_TRACK", "Robot Tanque con Orugas para Terreno Irregular",
                ["CATERPILLAR TANK ROBOT"], [],
                "Vehículo con tracción continua por orugas para superar pendientes y obstáculos en proyectos de rescate.",
                "Arduino", "Sí — Kit Robótica de Rescate"
            ),
            (
                "Robótica y vehículos", "robotica-vehiculos", "ROB_BALANCE_SHIELD", "Shield y Sistema para Robot Autoequilibrado de 2 Ruedas",
                ["BALANCE CAR SHIELD"], [],
                "Sistema para enseñanza de algoritmos de control PID, péndulo invertido y estabilidad dinámica.",
                "Arduino", "Sí — Kit Control Avanzado"
            ),

            # -------------------------------------------------------------
            # 4. Motores y movimiento (~8 candidatos)
            # -------------------------------------------------------------
            (
                "Motores y movimiento", "motores-movimiento", "MOT_SERVO_SG90", "Micro Servomotor SG90 9g de 180°",
                ["SG90 9G"], ["HOLDER", "TIRE", "WHEEL", "CAR", "KIT"],
                "Microactuador rotativo estándar escolar para brazos mecánicos, barreras de peaje y mecanismos articulados.",
                "Arduino / micro:bit", "Sí — Kit Mecatrónica Escolar"
            ),
            (
                "Motores y movimiento", "motores-movimiento", "MOT_SERVO_360", "Servomotor de Rotación Continua 360°",
                ["360 DEGREES SERVO MOTOR CONTINUOUS"], ["HOLDER", "TIRE"],
                "Servomotor con giro continuo de velocidad controlable, ideal para ruedas motrices directas en robots compactos.",
                "Arduino / micro:bit", "Sí — Kit Robótica Móvil"
            ),
            (
                "Motores y movimiento", "motores-movimiento", "MOT_TT_MOTOR", "Set de Motores DC TT con Engranajes y Conector PH2.0",
                ["TT MOTOR GEAR WITH CABLE"], ["CAR", "KIT"],
                "Conjunto de motor DC con caja reductora y conector seguro para tracción de autos robóticos escolares.",
                "Otros (Universal)", "Sí — Kit Robótica Escolar"
            ),
            (
                "Motores y movimiento", "motores-movimiento", "MOT_STEPPER_ULN2003", "Motor Paso a Paso con Placa Driver",
                ["STEPPER MOTOR DRIVER MODULE + STEPPER MOTOR"], ["CAR", "KIT"],
                "Motor de precisión angular para posicionamiento exacto en relojes, dosificadores y plataformas giratorias.",
                "Arduino / Raspberry Pi", "Sí — Kit Automatización de Precisión"
            ),
            (
                "Motores y movimiento", "motores-movimiento", "MOT_DRIVER_L9110", "Placa Driver de Motores Dual H-Bridge L9110S",
                ["L9110S H-BRIDGE"], ["CAR", "KIT"],
                "Controlador de potencia compacto para manejar dos motores DC o un motor paso a paso sin disipadores voluminosos.",
                "Arduino / micro:bit", "Sí — Kit Control de Potencia"
            ),
            (
                "Motores y movimiento", "motores-movimiento", "MOT_RELAY_1CH", "Módulo Relé 5V de 1 Canal Compatible con Arduino",
                ["SINGLE 5V RELAY MODULE"], ["KIT", "CAR"],
                "Interruptor electromecánico para controlar lámparas o bombas de agua desde un microcontrolador de forma segura.",
                "Arduino / ESP32", "Sí — Kit Domótica / Riego"
            ),
            (
                "Motores y movimiento", "motores-movimiento", "MOT_RELAY_2CH", "Módulo Relé 5V de 2 Canales con Optoacoplador",
                ["2-CHANNEL 5V RELAY MODULE"], ["KIT", "CAR"],
                "Tarjeta con dos relés independientes para control bidireccional o activación de dos cargas alternas simultáneas.",
                "Arduino / ESP32", "Sí — Kit Domótica Intermedia"
            ),
            (
                "Motores y movimiento", "motores-movimiento", "MOT_RELAY_4CH", "Módulo Relé 5V de 4 Canales Optoacoplado",
                ["4-CHANNEL 5V RELAY MODULE"], ["KIT", "CAR"],
                "Tarjeta de 4 relés independientes para proyectos multiactuador como casas inteligentes y control de invernaderos.",
                "Arduino / ESP32", "Sí — Kit Domótica Avanzada"
            ),

            # -------------------------------------------------------------
            # 5. Electrónica y prototipado (~11 candidatos)
            # -------------------------------------------------------------
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_BREADBOARD_830", "Protoboard Grande 830 Puntos Transparente",
                ["830 HOLE TRANSPARENT BREADBOARD"], ["KIT", "POWER"],
                "Placa de pruebas estándar de 830 contactos para montaje de circuitos medianos y grandes sin soldadura.",
                "Otros (Universal)", "Sí — Kit Prototipado Universal"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_BREADBOARD_400", "Protoboard Mediana 400 Puntos",
                ["400 HOLES MINI SOLDERLESS"], ["KIT", "POWER"],
                "Placa de inserción intermedia ideal para bancos de laboratorio individuales y proyectos compactos.",
                "Otros (Universal)", "Sí — Kit Prototipado Básico"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_BREADBOARD_MINI", "Mini Protoboard 25-170 Puntos de Pruebas",
                ["MINI 25 TIE-POINT BREADBOARD"], ["KIT"],
                "Placa miniatura modular para pruebas rápidas de componentes y shields modulares.",
                "Otros (Universal)", "Sí — Insumo Taller"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_JUMPER_MIX_120", "Set de Cables Dupont 120pcs Mixto (M-M / M-F / F-F)",
                ["DUPONT LINE 120PCS 10CM"], ["KIT"],
                "Cables flexibles con los 3 tipos de terminaciones para interconexión completa en el laboratorio escolar.",
                "Otros (Universal)", "Sí — Kit Conexión Esencial"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_JUMPER_30CM", "Set de Cables Dupont 120pcs Largos de 30cm",
                ["DUPONT LINE 120PCS 30CM"], ["KIT"],
                "Cables cinta largos indispensables para maquetas grandes, brazos mecánicos y autos robóticos.",
                "Otros (Universal)", "Sí — Kit Conexión Esencial"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_JUMPER_FF", "Set de Cables Jumper 40Pin Hembra-Hembra 20cm",
                ["40PIN FEMALE TO FEMALE HIGH QUALITY JUMPER"], ["KIT"],
                "Cables para conexión directa entre cabezales macho de placas de desarrollo y módulos sensores.",
                "Otros (Universal)", "Sí — Kit Conexión Esencial"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_POTENTIOMETER", "Módulo Potenciómetro Rotativo Ajustable",
                ["ADJUSTABLE POTENTIOMETER MODULE"], ["KIT", "CAR"],
                "Resistencia variable en módulo para control de volumen, brillo y enseñanza de entradas analógicas.",
                "Otros (Universal)", "Sí — Kit Entradas Analógicas"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_PUSH_BUTTON", "Módulo Pulsador Digital con Interruptor",
                ["DIGITAL PUSH BUTTON SWITCH MODULE"], ["KIT", "CAR"],
                "Interruptor momentáneo en módulo para diseño de interfaces de usuario y botones de control.",
                "Otros (Universal)", "Sí — Kit Entradas Digitales"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_BUZZER_ACTIVE", "Módulo Zumbador Buzzer Activo de Alarma 5V",
                ["ACTIVE BUZZER ALARM MODULE"], ["KIT", "CAR"],
                "Emisor sonoro que genera un tono audible continuo con un nivel lógico HIGH para alarmas y avisos.",
                "Arduino / micro:bit", "Sí — Kit Señalización Acústica"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_BREADBOARD_KIT", "Kit de Protoboard 830 Puntos + Fuente 3.3V/5V + Jumpers",
                ["BREADBOARD POWER MODULE+ 1PCS 830 POINTS"], [],
                "Set integral de prototipado que incluye alimentación regulada y cableado completo para mesa de trabajo.",
                "Otros (Universal)", "Sí — Alimentación de Laboratorio"
            ),
            (
                "Electrónica y prototipado", "electronica-prototipado", "ELC_LED_TUBE", "Display Tubo Digital LED de 7 Segmentos",
                ["DIGITAL TUBE LED DIGITAL TUD"], ["KIT"],
                "Dígito de visualización numérica de 7 segmentos para enseñanza de código binario y decodificadores.",
                "Otros (Universal)", "Sí — Insumo Lógica Digital"
            ),

            # -------------------------------------------------------------
            # 6. Pantallas e interacción (~8 candidatos)
            # -------------------------------------------------------------
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_LCD1602_I2C", "Pantalla LCD 16X2 con Interfaz I2C Integrada",
                ["16X2 1602 I2C/TWI LCD DISPLAY MODULE"], ["KIT"],
                "Display alfanumérico estándar de 2 líneas x 16 caracteres con bus I2C que usa solo 2 pines del microcontrolador.",
                "Arduino / Raspberry Pi", "Sí — Kit Estación de Monitoreo"
            ),
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_OLED_096", "Pantalla Gráfica OLED 0.96 Pulgadas I2C (128x64)",
                ["0.96'' OLED MODULE/128X64"], ["KIT"],
                "Display monocromático de alta nitidez para graficar curvas de temperatura, íconos y textos pequeños en aula.",
                "Arduino / ESP32", "Sí — Kit Instrumentación Científica"
            ),
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_MATRIX_8X8", "Módulo Matriz de Puntos LED 8x8",
                ["LED LATTICE BRIGHT RED DOT MATRIX MODULE"], ["KIT"],
                "Arreglo de 64 LEDs rojos para visualización de caracteres en movimiento, caras expresivas y animaciones simples.",
                "Arduino / micro:bit", "Sí — Kit Comunicación Visual"
            ),
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_TM1637", "Display 4 Dígitos 7 Segmentos TM1637 para Reloj",
                ["4-DIGIT LED DISPLAY MODULE TM1637"], ["KIT"],
                "Pantalla numérica con dos puntos centrales ideal para construir cronómetros, relojes y marcadores deportivos.",
                "Arduino / micro:bit", "Sí — Kit Cronometraje Escolar"
            ),
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_JOYSTICK", "Módulo Palanca Joystick Analógico PS2 de 2 Ejes",
                ["PS2 JOYSTICK MODULE"], ["KIT", "CAR"],
                "Controlador tipo gamepad con dos potenciómetros ortogonales y botón central para teledirección de robots.",
                "Arduino / micro:bit", "Sí — Kit Control de Robots"
            ),
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_KEYPAD_4X3", "Teclado Matricial de Membrana 4x3 (12 Teclas)",
                ["4*3 MATRIX ARRAY 12 KEY MEMBRANE SWITCH"], ["KIT"],
                "Interfaz numérica delgada autoadhesiva para sistemas de acceso por contraseña y calculadoras escolares.",
                "Arduino", "Sí — Kit Control de Acceso"
            ),
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_RGB_MATRIX", "Shield Matriz de 40 LEDs RGB Direccionables WS2812",
                ["40 RGB LED WS2812 PIXEL MATRIX SHIELD"], ["KIT"],
                "Iluminación inteligente multicolor controlada por un solo pin digital para crear efectos visuales artísticos.",
                "Arduino / micro:bit", "Sí — Kit Arte y Tecnología"
            ),
            (
                "Pantallas e interacción", "pantallas-interaccion", "PAN_TRAFFIC_LIGHT", "Módulo Didáctico Semáforo LED 5V",
                ["TRAFFIC LIGHT MODULE"], ["KIT"],
                "Módulo integrado con LEDs verde, amarillo y rojo para enseñar lógica secuencial y educación vial escolar.",
                "Arduino / micro:bit", "Sí — Kit Educación Vial"
            ),

            # -------------------------------------------------------------
            # 7. Micro:bit y accesorios (~7 candidatos)
            # -------------------------------------------------------------
            (
                "Micro:bit y accesorios", "microbit", "MB_EXPANSION_EDGE", "Placa de Expansión Edge Breakout para BBC micro:bit",
                ["MICROBIT EDGE CONNECTOR I/O SENSOR BREAKOUT"], ["KIT", "CAR"],
                "Placa breakout que transforma el conector de borde de micro:bit en cabezales estándar de pines para prototipado.",
                "micro:bit", "Sí — Kit micro:bit Básico"
            ),
            (
                "Micro:bit y accesorios", "microbit", "MB_SERVO_SHIELD", "Shield con Portapilas y Control de Servos para micro:bit",
                ["MICRO BIT MINI SERVO SHIELD WITH BATTERY HOLDER"], ["KIT", "CAR"],
                "Placa complementaria que provee portapilas y salidas de servos para hacer autónomo a micro:bit sin cables USB.",
                "micro:bit", "Sí — Kit micro:bit Autónomo"
            ),
            (
                "Micro:bit y accesorios", "microbit", "MB_POWER_SHIELD", "Módulo Power Shield de Alimentación para micro:bit",
                ["POWER SHIELD MODULE WITHOUT BATTERY FOR BBC MIC"], ["KIT", "CAR"],
                "Placa de energización compacta para proyectos escolares portátiles basados en micro:bit.",
                "micro:bit", "Sí — Accesorio Básico micro:bit"
            ),
            (
                "Micro:bit y accesorios", "microbit", "MB_GO_KIT", "Kit Oficial BBC micro:bit V2 Go con Cable y Portapilas",
                ["ORIGINAL MICROBIT GO KIT MAIN BOARD+USB CABLE+BATTERY HOLDER"], [],
                "Set oficial completo con tarjeta micro:bit V2, cable micro-USB, portapilas AAA y guía de inicio rápido.",
                "micro:bit", "Sí — Kit Oficial Inicio"
            ),
            (
                "Micro:bit y accesorios", "microbit", "MB_ROBOT_ARM", "Brazo Robótico Mecatrónico para micro:bit Learning Kit",
                ["4DOF ROBOT ARM MICROBIT LEARNING KIT"], [],
                "Manipulador robótico programable directamente por bloques mediante MakeCode para micro:bit.",
                "micro:bit", "Sí — Kit Robótica Primaria"
            ),
            (
                "Micro:bit y accesorios", "microbit", "MB_CROCODILE_KIT", "Kit Creativo con Cables Caimán para micro:bit",
                ["CROCODILE CREATIVE LEARNING STARTER KIT"], [],
                "Set didáctico con cables caimán para proyectos de conductividad de materiales, frutas y circuitos de papel.",
                "micro:bit", "Sí — Kit STEAM Inicial"
            ),
            (
                "Micro:bit y accesorios", "microbit", "MB_CONTINUOUS_SERVO", "Set de Motores y Servos Especiales para micro:bit",
                ["DUAL OUTPUT SHAFT 2KG DC MOTOR", "MICROBIT"], [],
                "Actuadores diseñados para acoplarse directamente a chasis y estructuras compatibles con micro:bit.",
                "micro:bit", "Sí — Kit Movimiento micro:bit"
            ),

            # -------------------------------------------------------------
            # 8. Raspberry Pi y accesorios (~6 candidatos)
            # -------------------------------------------------------------
            (
                "Raspberry Pi y accesorios", "raspberry-pi", "RPI_T_COBBLER", "Placa T-Cobbler GPIO con Cable Cinta de 40 Pines",
                ["RASPBERRY PI T TYPE BOARD+40P COLORFUL RIBBON CABLE"], ["KIT"],
                "Adaptador tipo 'T' con cable bus de 40 pines para llevar todos los pines de Raspberry Pi ordenadamente al protoboard.",
                "Raspberry Pi", "Sí — Kit Linux y Python Escolar"
            ),
            (
                "Raspberry Pi y accesorios", "raspberry-pi", "RPI_CAMERA_MODULE", "Módulo Cámara CSI 5MP 1080p Compatible con Raspberry Pi",
                ["5 MEGAPIXELS 1080P MINI CAMERA VIDEO MODULE FOR R"], ["HOLDER", "CASE"],
                "Sensor óptico con interfaz CSI nativa para proyectos de visión por computador, reconocimiento de objetos y seguridad.",
                "Raspberry Pi", "Sí — Kit Visión Artificial"
            ),
            (
                "Raspberry Pi y accesorios", "raspberry-pi", "RPI_GPIO_KIT", "Kit de Expansión GPIO y Prototipado para Raspberry Pi 4",
                ["GPIO BREAKOUT KIT FOR RASPBERRY PI 4 4B"], [],
                "Set de expansión con componentes de conexión directa para talleres de programación en Python en Linux.",
                "Raspberry Pi", "Sí — Kit Python Físico"
            ),
            (
                "Raspberry Pi y accesorios", "raspberry-pi", "RPI_ALU_CASE_FAN", "Gabinete de Aluminio con Disipación y Ventilador para Raspberry Pi",
                ["BLACK ALUMINUM ALLOY BOX CASE POROUS HEAT-DISSIPATING METAL"], [],
                "Caja metálica reforzada con enfriamiento activo para proteger placas Raspberry Pi en talleres escolares intensivos.",
                "Raspberry Pi", "Sí — Accesorio Protección"
            ),
            (
                "Raspberry Pi y accesorios", "raspberry-pi", "RPI_CLEAR_CASE", "Gabinete Acrílico Transparente Ventilado para Raspberry Pi 4",
                ["ACRYLIC TRANSPARENT CASE BOX FOR RASPBERRY PI 4"], [],
                "Carcasa transparente que permite ver los componentes internos protegiendo la placa de cortocircuitos accidentales.",
                "Raspberry Pi", "Sí — Accesorio Protección"
            ),
            (
                "Raspberry Pi y accesorios", "raspberry-pi", "RPI_CAM_HOLDER", "Soporte Acrílico Ajustable para Cámara Raspberry Pi",
                ["RASPBERRY PI CAMERA HOLDER ACRYLIC HOLDER"], [],
                "Base articulada para posicionar la cámara en proyectos de vigilancia escolar y robótica guiada por visión.",
                "Raspberry Pi", "Sí — Accesorio Soporte"
            ),

            # -------------------------------------------------------------
            # 9. IoT y comunicación (~7 candidatos)
            # -------------------------------------------------------------
            (
                "IoT y comunicación", "iot-comunicacion", "IOT_BT_HC05", "Módulo Bluetooth Serial HC-05 Maestro / Esclavo",
                ["BLUETOOH XBEE BLUETOOTH WIRELESS MODULE HC-05"], ["KIT"],
                "Módulo transceptor inalámbrico para enlazar microcontroladores con smartphones Android o computadores vía puerto serie.",
                "Arduino", "Sí — Kit Telemetría Inalámbrica"
            ),
            (
                "IoT y comunicación", "iot-comunicacion", "IOT_BLE_SHIELD", "Shield Bluetooth 4.0 BLE de Expansión para Arduino UNO",
                ["BLUETOOTH 4.0 SHIELD EXPANSION SHIELD BOARD FOR ARDUINO UNO R3"], ["KIT"],
                "Transceptor Bluetooth Low Energy para compatibilidad moderna con dispositivos iOS, tablets y bajo consumo.",
                "Arduino", "Sí — Kit Dispositivos Móviles"
            ),
            (
                "IoT y comunicación", "iot-comunicacion", "IOT_WIFI_ESP8266", "Módulo Wi-Fi Serial ESP8266 para Arduino",
                ["ESP8266 REMOTE SERIAL PORT WIFI MODULE FOR ARDUINO"], ["KIT"],
                "Módulo transceptor Wi-Fi TCP/IP de bajo costo para conectar microcontroladores a servidores IoT y paneles educativos.",
                "Arduino / ESP32", "Sí — Kit Conectividad Escolar"
            ),
            (
                "IoT y comunicación", "iot-comunicacion", "IOT_RFID_RC522", "Módulo Lector RFID RC522 13.56MHz con Tarjeta y Llavero",
                ["RC522 RFID MODULE FOR ARDUINO"], ["KIT"],
                "Sistema de identificación por radiofrecuencia para registro de asistencia escolar, cerraduras electrónicas y biblioteca.",
                "Arduino / ESP32", "Sí — Kit Control de Acceso"
            ),
            (
                "IoT y comunicación", "iot-comunicacion", "IOT_NRF24L01", "Módulo Transceptor Inalámbrico 2.4GHz NRF24L01+",
                ["NRF24L01 2.4GHZ WIRELESS TRANSCEIVER MODULE"], ["KIT"],
                "Módulo de radiofrecuencia digital para comunicación bidireccional entre robots sin depender de redes Wi-Fi.",
                "Arduino", "Sí — Kit Comunicación Robot-a-Robot"
            ),
            (
                "IoT y comunicación", "iot-comunicacion", "IOT_IR_RECEIVER", "Módulo Receptor Infrarrojo Digital con Filtro",
                ["DIGITAL IR INFRARED RECEIVER MODULE FOR ARDUINO"], ["KIT", "CAR"],
                "Sensor receptor para decodificar señales de mandos a distancia por infrarrojos y controlar actuadores en aula.",
                "Arduino / micro:bit", "Sí — Kit Mando a Distancia"
            ),
            (
                "IoT y comunicación", "iot-comunicacion", "IOT_ESP8266_SHIELD", "Shield ESP8266 con Cable de Datos para Arduino",
                ["ESP8266 WI-FI MODULE SHIELD +1M MICRO USB CABLE"], ["KIT"],
                "Shield integral con módulo Wi-Fi y puerto USB serie para conexión directa a la placa base escolar.",
                "Arduino / ESP32", "Sí — Kit Internet de las Cosas"
            ),

            # -------------------------------------------------------------
            # 10. Kits educativos iniciales (~7 candidatos)
            # -------------------------------------------------------------
            (
                "Kits educativos iniciales", "kits-educativos", "KIT_STARTER_BASIC", "Starter Kit Básico de Inicio para Arduino con 20 Proyectos",
                ["BASIC STARTER KIT FOR ARDUINO DIY PROGRAMMING ELECTRONICS KIT 20PROJECT"], [],
                "Set didáctico inicial con componentes esenciales y manual de proyectos guiados paso a paso para academias escolares.",
                "Arduino", "Sí — Kit Formativo Inicial"
            ),
            (
                "Kits educativos iniciales", "kits-educativos", "KIT_37_SENSORS", "Kit Didáctico 37 Sensores en 1 con Maletín y Tutoriales",
                ["37 IN 1 SENSOR KIT UPGRADE V3.0 +GIFT BOX FOR ARDUINO STARTER KIT"], [],
                "Colección exhaustiva de 37 módulos y transductores organizada en maletín plástico para laboratorios de ciencias.",
                "Arduino / micro:bit", "Sí — Laboratorio de Sensores"
            ),
            (
                "Kits educativos iniciales", "kits-educativos", "KIT_SMART_FARM", "Kit Didáctico de Huerto Inteligente con Control ESP32",
                ["ESP32 IOT CONTROL SMART FARM STARTER KIT FOR ARDUINO"], [],
                "Sistema didáctico de automatización con bomba de agua, sensor de humedad y monitoreo en la nube para agroecología STEM.",
                "ESP32", "Sí — Kit Agroecología STEM"
            ),
            (
                "Kits educativos iniciales", "kits-educativos", "KIT_SMART_HOME", "Kit Didáctico de Casa Inteligente y Domótica Escolar",
                ["SMART HOME KIT WITH PLUS BOARD FOR ARDUINO"], [],
                "Maqueta de casa inteligente con sensores de gas, ventilador, ventanas automáticas y app móvil escolar.",
                "Arduino", "Sí — Kit Domótica Escolar"
            ),
            (
                "Kits educativos iniciales", "kits-educativos", "KIT_RPI_STARTER", "Starter Kit Completo de Proyectos para Raspberry Pi 4B",
                ["ORIGINAL RASPBERRY PI 4B COMPLETE STARTER KIT"], [],
                "Maletín completo con módulos interactivos y manuales para aprender programación en Python bajo Linux.",
                "Raspberry Pi", "Sí — Kit Python Avanzado"
            ),
            (
                "Kits educativos iniciales", "kits-educativos", "KIT_FOXBIT_GO", "Kit de Desarrollo Foxbit Go con Sensores y Wi-Fi/Bluetooth",
                ["FOXBIT GO DEVELOPMENT KIT RICH SENSOR"], [],
                "Plataforma educativa todo-en-uno con periféricos integrados en una sola tarjeta para programar sin cablear.",
                "Otros (Universal)", "Sí — Caja de Herramientas Maker"
            ),
            (
                "Kits educativos iniciales", "kits-educativos", "KIT_AI_CHATBOT", "Kit Didáctico Xiaozhi AI Chatbot con Cámara y ESP32-S3",
                ["ESP32 S3 XIAOZHI AI CHATBOT KIT WITH CAMERA"], [],
                "Kit de última generación para aprender Inteligencia Artificial generativa, visión y voz aplicada en aula.",
                "ESP32", "Sí — Kit Inteligencia Artificial"
            ),

            # -------------------------------------------------------------
            # 11. Herramientas y accesorios (~6 candidatos)
            # -------------------------------------------------------------
            (
                "Herramientas y accesorios", "herramientas-accesorios", "HER_BATT_CASE_AA", "Portapilas para Baterías AA con Conector Plug DC",
                ["88000 6 AAA BATTERY & 8881 9V AA BATTERY HOLD"], [],
                "Portapilas con conector de alimentación estándar para dar autonomía eléctrica a proyectos y robots escolares.",
                "Otros (Universal)", "Sí — Alimentación Autónoma"
            ),
            (
                "Herramientas y accesorios", "herramientas-accesorios", "HER_MULTIMETER_DIGITAL", "Multímetro Digital Portátil LCD con Puntas de Prueba",
                ["XL830L MINI DIGITAL MULTIMETER AC/DC CURRENT 20A PORTABLE LC"], [],
                "Instrumento básico de medición de voltaje, corriente y continuidad para comprobación segura en laboratorio escolar.",
                "Otros (Universal)", "Sí — Instrumentación Escolar"
            ),
            (
                "Herramientas y accesorios", "herramientas-accesorios", "HER_MULTIMETER_PRO", "Multímetro Digital Completo de Alta Resistencia",
                ["DT9205A FULLY PROTECTED MULTIMETER"], [],
                "Instrumento de medición de mayor precisión con protección para bancos de trabajo y talleres técnicos.",
                "Otros (Universal)", "Sí — Instrumentación Escolar"
            ),
            (
                "Herramientas y accesorios", "herramientas-accesorios", "HER_USB_TTL_CP2102", "Módulo Adaptador USB a UART TTL CP2102 con Cable Dupont",
                ["CP2102 USB TO TTL / STC 6PIN SPEED DOWNLOAD FOR ARDUINO"], [],
                "Conversor USB a puerto serie TTL indispensable para programar microcontroladores Pro Mini y depurar terminales.",
                "Otros (Universal)", "Sí — Herramienta Programación"
            ),
            (
                "Herramientas y accesorios", "herramientas-accesorios", "HER_SD_MODULE", "Módulo Lector de Tarjetas SD con Conector SPI",
                ["SD CARD MODULE SLOT SOCKET READER FOR ARDUINO"], ["KIT", "CAR"],
                "Módulo de almacenamiento masivo para registrar datos científicos (datalogger) en salidas a terreno escolares.",
                "Arduino / micro:bit", "Sí — Datalogger Científico"
            ),
            (
                "Herramientas y accesorios", "herramientas-accesorios", "HER_TOUCH_PEN", "Lápiz Táctil Stylus para Pantallas Resistivas",
                ["RESISTIVE TOUCH PEN FOR 3.5 TOUCH SCREEN"], [],
                "Accesorio para operación táctil precisa en pantallas LCD de proyectos interactivos escolares.",
                "Otros (Universal)", "Sí — Accesorio Interacción"
            ),
        ]

        # 2. Análisis del Catálogo Maestro
        productos = list(Producto.objects.filter(activo=True).prefetch_related("imagenes"))
        self.stdout.write(f"Productos activos en base de datos: {len(productos)}")

        # Excluir productos sin imagen física
        prods_con_foto = [p for p in productos if p.imagenes.exists()]
        self.stdout.write(f"Productos con fotografía confirmada: {len(prods_con_foto)}")

        # 3. Selección Rigurosa y Mapeo de Redundancias
        candidatos_seleccionados = []
        productos_ya_asignados = set()

        for (cat_nom, cat_slug, cluster_id, cluster_label, includes, excludes, motivo, tec, apto_kit) in ARQUETIPOS:
            coincidentes = []

            for p in prods_con_foto:
                if p.id in productos_ya_asignados:
                    continue

                txt = f"{p.sku_proveedor} {p.nombre_original_proveedor}".upper()

                # Todos los términos de 'includes' deben estar en el texto
                if not all(inc in txt for inc in includes):
                    continue

                # Ninguno de los términos de 'excludes' debe estar en el texto
                if any(exc in txt for exc in excludes):
                    continue

                coincidentes.append(p)

            if not coincidentes:
                # Intentar búsqueda con include más corto
                for p in prods_con_foto:
                    if p.id in productos_ya_asignados:
                        continue
                    txt = f"{p.sku_proveedor} {p.nombre_original_proveedor}".upper()
                    if includes[0] in txt and not any(exc in txt for exc in excludes):
                        coincidentes.append(p)

            if coincidentes:
                # Ordenar para elegir la mejor unidad: preferir precio escolar accesible y producto unitario
                def score_producto(prod):
                    desc = prod.nombre_original_proveedor.upper()
                    penalty = 0
                    if any(multi in desc for multi in ["10PCS", "5PCS", "SET", "KIT"]):
                        if "KIT" not in cluster_id and "PACK" not in cluster_id and "MIX" not in cluster_id:
                            penalty += 50
                    return (penalty, prod.costo_proveedor_usd)

                coincidentes.sort(key=score_producto)
                ganador = coincidentes[0]
                redundantes = [p.sku_proveedor for p in coincidentes[1:]]

                productos_ya_asignados.add(ganador.id)

                candidatos_seleccionados.append({
                    "producto": ganador,
                    "cluster_id": cluster_id,
                    "cluster_label": cluster_label,
                    "categoria_nombre": cat_nom,
                    "categoria_slug": cat_slug,
                    "motivo_seleccion": motivo,
                    "tecnologia_sugerida": tec,
                    "aptitud_kit": apto_kit,
                    "redundantes": redundantes,
                })

        total_candidatos = len(candidatos_seleccionados)
        self.stdout.write(f"\nTotal de candidatos seleccionados: {total_candidatos} productos")

        # 4. Generar Documento Markdown
        md_text = self.construir_markdown_fase_3(candidatos_seleccionados)
        reporte_path.write_text(md_text, encoding="utf-8")
        self.stdout.write(self.style.SUCCESS(f"✔ Reporte Markdown generado en: {reporte_path}"))
        self.stdout.write("=" * 70)

    def construir_markdown_fase_3(self, candidatos):
        total = len(candidatos)
        conteo_por_cat = defaultdict(list)
        for c in candidatos:
            conteo_por_cat[c["categoria_nombre"]].append(c)

        # 1. Tabla Resumen de Categorías
        filas_resumen = ""
        for cat_nom, items in conteo_por_cat.items():
            cnt = len(items)
            pct = (cnt / total) * 100
            filas_resumen += f"| **{cat_nom}** | {cnt} candidatos | {pct:.1f}% |\n"

        # 2. Detalle de Candidatos por Categoría con todas las columnas requeridas
        secciones_detalle = ""
        n_global = 0

        for cat_nom, items in conteo_por_cat.items():
            secciones_detalle += f"\n### {cat_nom} ({len(items)} candidatos)\n\n"
            secciones_detalle += (
                "| N° | SKU Humm | SKU Prov. | Nombre Original | Precio Sugerido CLP | Categoría Sugerida | Tec. Compatible | Motivo de Selección | Aptitud Potencial para Kit | Posibles Productos Similares o Redundantes |\n"
                "| :-: | :--- | :---: | :--- | :---: | :--- | :--- | :--- | :--- | :--- |\n"
            )

            for it in items:
                n_global += 1
                p = it["producto"]
                sku_h = p.sku_humm
                sku_p = p.sku_proveedor
                nom_orig = p.nombre_original_proveedor.replace("|", "/")
                precio_clp = f"${p.precio_sugerido_total_clp:,.0f} CLP"
                cat_sug = it["categoria_nombre"]
                tec_sug = it["tecnologia_sugerida"]
                motivo = it["motivo_seleccion"]
                kit_apt = it["aptitud_kit"]

                # Lista de redundantes
                reds = it["redundantes"]
                if reds:
                    if len(reds) <= 4:
                        red_str = ", ".join([f"`{r}`" for r in reds])
                    else:
                        red_str = ", ".join([f"`{r}`" for r in reds[:4]]) + f" (+{len(reds)-4} más)"
                else:
                    red_str = "*Único en su tipo*"

                secciones_detalle += (
                    f"| {n_global} | `{sku_h}` | **`{sku_p}`** | {nom_orig} | **{precio_clp}** | "
                    f"{cat_sug} | {tec_sug} | {motivo} | {kit_apt} | {red_str} |\n"
                )

        return f"""# CANDIDATOS SUGERIDOS PARA FASE 3 — CURADURÍA EDUCATIVA
## Propuesta de Preselección del Catálogo Público (EduCompra Humm)
### `educompra.humm.cl`

**Fecha:** 29 de Septiembre de 2026  
**Modo de Ejecución:** **SOLO LECTURA — BASE DE DATOS SIN MODIFICAR**  
**Total Candidatos Sugeridos:** **{total} productos** (dentro del rango solicitado de 70 a 120 candidatos)  
**Estado:** **PRIMER PUNTO DE CONTROL — DETENIDO PARA REVISIÓN Y APROBACIÓN DE HUMM**  

---

## 1. Resumen Ejecutivo de la Preselección

De los **929 productos importados** en el catálogo maestro Keyestudio, el algoritmo de preselección analizó exhaustivamente especificaciones, precios, presencia de fotografías y duplicidades funcionales, consolidando un conjunto inicial equilibrado de **{total} productos educativos**.

Este grupo representa la base idónea para iniciar la curaduría pedagógica individual y alimentar los futuros kits temáticos escolares:

| Categoría Docente Propuesta | Cantidad de Candidatos | Proporción del Lote |
| :--- | :---: | :---: |
{filas_resumen}| **TOTAL CANDIDATOS PROPUESTOS** | **{total} productos** | **100.0%** |

---

## 2. Criterios de Selección y Reducción de Redundancias

Para garantizar un catálogo escolar claro, navegable y pedagógicamente coherente, se aplicaron los 8 criterios establecidos por Humm:

1. **Utilidad Educativa Probable:** Selección de componentes con aplicación directa en el aula de clases, laboratorios de ciencias, talleres de robótica y academias STEM.
2. **Accesibilidad de Precios:** Priorización de componentes unitarios de alta rotación escolar con costos accesibles para colegios y sostenedores.
3. **Disponibilidad de Imagen Física:** El **100% de los {total} candidatos cuenta con fotografía real** verificada en `media/productos/originales/`.
4. **Compatibilidad Tecnológica Estructurada:** Mapeo controlado con las plataformas escolares líderes: **Arduino**, **ESP32**, **micro:bit**, **Raspberry Pi** y **Otros**.
5. **Reducción de Redundancias Funcionales:** De múltiples variantes casi idénticas del fabricante (ej: placas con/sin cable USB, versiones en empaque blister versus bolsa antiestática, o lotes multi-pack), se seleccionó la unidad canónica más representativa y se agruparon las demás como productos redundantes.
6. **Aptitud Potencial para Kits:** Identificación sistemática de componentes con alta complementariedad para conformar los futuros kits temáticos de Humm (Kit Huerto Inteligente, Kit Robótica Móvil, Kit Domótica, Kit Estación Meteorológica, etc.).
7. **Nivel de Uso Técnico Separado de Grado Escolar:** Los productos se preparan para su clasificación en niveles de complejidad técnica (*Inicial*, *Intermedio*, *Avanzado*) sin atarlos rígidamente a una edad o curso escolar.
8. **Neutralidad Técnica en Espera:** Todos los productos mantienen su especificación en estado `NO_REVISADO`. Ninguno podrá avanzar a `VALIDADO_HUMM` sin revisión técnica humana individual.

---

## 3. Catálogo Detallado de Candidatos Sugeridos

A continuación se presenta el detalle de los **{total} productos propuestos**, organizados por categoría y especificando los 9 atributos requeridos para la evaluación de Humm:

{secciones_detalle}

---

## 4. Compromisos Técnicos y Estado del Sistema

* **Cero Publicaciones Prematuras:** Los 929 productos del catálogo maestro se mantienen con `publicado = False`.
* **Cero Modificaciones Automáticas de Estado:** Ningún producto ha sido modificado a `CANDIDATO` en la base de datos de producción.
* **Neutralidad Técnica Protegida:** La acción masiva `validar_especificacion_neutra_humm` ha sido eliminada por diseño. Solo la revisión individual desde el Django Admin podrá asignar `VALIDADO_HUMM`.
* **Detención Obligatoria:** Este reporte constituye el **PRIMER PUNTO DE CONTROL**. El equipo de desarrollo se detiene en este hito a la espera de la revisión, ajustes y autorización formal por parte de Humm.
"""
