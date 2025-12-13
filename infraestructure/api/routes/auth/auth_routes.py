from flask import Blueprint, request, jsonify
from sqlalchemy import text
from werkzeug.security import check_password_hash

from infraestructure.config.config_bd import engine
from infraestructure.security.token_manager import generar_token

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    nameuser = data.get("nameuser")
    password = data.get("password")

    if not nameuser or not password:
        return jsonify({"error": "Faltan credenciales"}), 400

    try:
        with engine.connect() as connectionBD:
            # Corregido: usar el mismo nombre de parámetro
            user = connectionBD.execute(
                text("SELECT * FROM usuarios WHERE nameuser = :nameuser"),
                {"nameuser": nameuser}
            ).mappings().first()

            if not user:
                return jsonify({"error": "Usuario no encontrado"}), 404

            # Validamos contraseña
            if not check_password_hash(user["passwordhash"], password):
                return jsonify({"error": "Contraseña incorrecta"}), 401

            # Generar JWT
            token = generar_token(user["id"], user["rol"])

            return jsonify({
                "status": 200,
                "message": "Login correcto",
                "token": token,
                "usuario": {
                    "id": user["id"],
                    "nameuser": user["nameuser"],
                    "email": user["email"],
                    "rol": user["rol"]
                }
            }), 200

    except Exception as e:
        print("❌ ERROR LOGIN:", e)
        return jsonify({"error": str(e)}), 500
