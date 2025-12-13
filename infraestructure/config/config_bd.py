#infraestructure/config/config_bd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infraestructure.config.settings import settings

# Crear el engine con la cadena de conexion
engine = create_engine(settings.DATABASE_URL, echo=True)

# Crear una sesion local (cada request puede usar una)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)