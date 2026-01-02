import io
import json
import os

from flask import Flask, redirect, send_from_directory
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from infraestructure.api.routes.auth.auth_routes import auth_bp
from infraestructure.api.routes.metricsport.metric_sport_routes import metrics_person_bp
from infraestructure.api.routes.sport.sport_routes import sport_bp
from infraestructure.api.routes.uploadfiles.uploadfile_routes import upload_bp
from infraestructure.api.routes.user.user_routes import user_bp

from infraestructure.config.settings import settings


# ============================================================
#  RUTAS BASE DEL PROYECTO
# ============================================================
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
OPENAPI_DIR = os.path.join(BASE_DIR, "infraestructure", "api", "docs")
OPENAPI_FILE = "openapi.json"

# ============================================================
#  Crear la aplicación Flask
# ============================================================
app = Flask(__name__)
CORS(app)


# ============================================================
#  Verificar que openapi.json se carga correctamente
# ============================================================
openapi_path = os.path.join(OPENAPI_DIR, OPENAPI_FILE)

try:
    with io.open(openapi_path, "r", encoding="utf-8") as f:
        json.load(f)
except Exception as e:
    print("⚠️ Error al leer openapi.json:", e)


# ============================================================
#  Blueprints de la API
# ============================================================
app.register_blueprint(auth_bp)
app.register_blueprint(sport_bp)
app.register_blueprint(metrics_person_bp)
app.register_blueprint(user_bp)
app.register_blueprint(upload_bp)
print("📌 RUTAS REGISTRADAS:")
print(f'La ruta es -----------> {app.url_map}')


# ============================================================
#  Endpoint que sirve el JSON OpenAPI
# ============================================================
@app.route("/docs/openapi.json")
def openapi_json():
    return send_from_directory(OPENAPI_DIR, OPENAPI_FILE)


# ============================================================
#  Configuración de Swagger UI
# ============================================================
SWAGGER_URL = settings.SWAGGER_URL          # Ej: "/swagger"
API_URL = "/docs/openapi.json"              # URL que apunta a tu JSON real

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={"app_name": settings.APP_NAME}
)

app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)


# ============================================================
#  Redirección principal
# ============================================================
@app.route("/")
def index():
    return redirect(SWAGGER_URL)


# ============================================================
#  Iniciar aplicación
# ============================================================
if __name__ == "__main__":
    print("🔥 Ejecutando SportPerformance Flask...")
    print(f"📘 Swagger UI: http://localhost:5000{SWAGGER_URL}")
    print(f"📄 OpenAPI JSON: http://localhost:5000/docs/openapi.json")
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)
