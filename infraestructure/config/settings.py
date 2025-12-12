import os
from dotenv import load_dotenv

# Cargar variables desde el archivo .env
load_dotenv()


class Settings:
    # Configuracion general de Flask
    APP_NAME = "sportPerformance API"
    DEBUG = True

    # Swagger
    SWAGGER_URL = "/swagger"
    API_URL = "/static/swagger.json"

    # Base del proyecto
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # API externas (opcional)
    API_KEY = os.getenv("API_KEY")

    # Configuracion de la base de datos PostgreSQL
    DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/sportPerformance"


# Instancia global de configuracion
settings = Settings()
