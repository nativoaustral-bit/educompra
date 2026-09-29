#!/home1/paulocis/apps/educompra/venv/bin/python
import os
import sys
from dotenv import load_dotenv

# Priorizar directorios de la aplicación
app_dir = "/home1/paulocis/apps/educompra/app"
if os.path.exists(app_dir) and app_dir not in sys.path:
    sys.path.insert(0, app_dir)
else:
    local_dir = os.path.dirname(os.path.abspath(__file__))
    if local_dir not in sys.path:
        sys.path.insert(0, local_dir)

# Cargar variables de entorno exclusivas de producción
env_file = "/home1/paulocis/apps/educompra/secrets/.env"
if os.path.exists(env_file):
    load_dotenv(env_file)
elif os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")):
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))

# Asegurar rutas persistentes en HostGator
if "DB_NAME" not in os.environ and os.path.exists("/home1/paulocis/apps/educompra/data"):
    os.environ["DB_NAME"] = "/home1/paulocis/apps/educompra/data/db.sqlite3"
if "MEDIA_ROOT" not in os.environ and os.path.exists("/home1/paulocis/apps/educompra/media"):
    os.environ["MEDIA_ROOT"] = "/home1/paulocis/apps/educompra/media"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

from config.wsgi import application as _application

def application(environ, start_response):
    environ["SCRIPT_NAME"] = ""
    return _application(environ, start_response)

if __name__ == "__main__" or "GATEWAY_INTERFACE" in os.environ:
    from wsgiref.handlers import CGIHandler
    CGIHandler().run(application)
