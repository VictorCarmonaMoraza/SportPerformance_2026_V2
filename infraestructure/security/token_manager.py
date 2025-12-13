import jwt
from datetime import datetime, timedelta

# Clave secreta para firmar los tokens
SECRET_KEY = "super_clave_secreta_sportperformance"

def generar_token(user_id, rol):
    """Genera un token JWT válido por 24 horas."""

    payload = {
        "user_id": user_id,
        "rol": rol,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "iat": datetime.utcnow()
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token
