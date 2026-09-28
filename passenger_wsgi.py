import os
import sys

# Definición de rutas operativas en el servidor HostGator
APP_PATH = "/home1/paulocis/apps/educompra/app"
SECRETS_FILE = "/home1/paulocis/apps/educompra/secrets/.env"

# Asegurar que el directorio de la aplicación esté en el path de Python
if os.path.exists(APP_PATH) and APP_PATH not in sys.path:
    sys.path.insert(0, APP_PATH)
else:
    # Ruta local de respaldo si se ejecuta en entorno de desarrollo
    local_path = os.path.dirname(os.path.abspath(__file__))
    if local_path not in sys.path:
        sys.path.insert(0, local_path)

# Cargar variables de entorno de producción si el archivo existe
if os.path.exists(SECRETS_FILE):
    from dotenv import load_dotenv
    load_dotenv(SECRETS_FILE)
elif os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")):
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
