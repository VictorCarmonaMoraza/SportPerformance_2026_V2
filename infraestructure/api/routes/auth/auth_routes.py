from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from infraestructure.config.config_bd import engine
from infraestructure.security.token_manager import generar_token
from sqlalchemy import text


auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    nameuser = data.get("nameuser")
    password = data.get("password")

    if not nameuser or not password:
        return jsonify({
            "status": 400,
            "error": "Faltan credenciales"
        }), 400

    try:
        with engine.connect() as connectionBD:

            user = connectionBD.execute(
                text("""
                    SELECT
                        id,
                        nameuser,
                        email,
                        passwordhash,
                        rol,
                        foto_url
                    FROM usuarios
                    WHERE nameuser = :nameuser
                """),
                {"nameuser": nameuser}
            ).mappings().first()

            if not user:
                return jsonify({
                    "status": 404,
                    "error": "Usuario no encontrado"
                }), 404

            if not check_password_hash(user["passwordhash"], password):
                return jsonify({
                    "status": 401,
                    "error": "Contraseña incorrecta"
                }), 401

            token = generar_token(user["id"], user["rol"])

            tiene_foto = user["foto_url"] is not None

            return jsonify({
                "status": 200,
                "message": "Login correcto",
                "token": token,
                "user": {
                    "id": user["id"],
                    "nameuser": user["nameuser"],
                    "email": user["email"],
                    "rol": user["rol"],
                    "tiene_foto": tiene_foto,
                    "foto_url": user["foto_url"]
                }
            }), 200

    except Exception as e:
        print("❌ ERROR LOGIN:", e)
        return jsonify({
            "status": 500,
            "error": "Error interno del servidor",
            "detail": str(e)
        }), 500



@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    nameuser = data.get("nameuser")
    email = data.get("email")
    password = data.get("password")

    if not nameuser or not email or not password:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    try:
        password_hash = generate_password_hash(password)

        with engine.begin() as connectionBD:

            # 1️⃣ Comprobar si existe usuario
            existing_user = connectionBD.execute(
                text("""
                    SELECT id 
                    FROM usuarios 
                    WHERE nameuser = :nameuser OR email = :email
                """),
                {"nameuser": nameuser, "email": email}
            ).fetchone()

            if existing_user:
                return jsonify({"error": "El usuario o email ya existe"}), 409

            # 2️⃣ Insertar usuario y recuperar ID
            result = connectionBD.execute(
                text("""
                    INSERT INTO usuarios (nameuser, email, passwordhash)
                    VALUES (:nameuser, :email, :passwordhash)
                    RETURNING id
                """),
                {
                    "nameuser": nameuser,
                    "email": email,
                    "passwordhash": password_hash
                }
            )

            usuario_id = result.scalar()

            # 3️⃣ Insertar SOLO el usuario_id en deportista
            connectionBD.execute(
                text("""
                    INSERT INTO deportistas (usuario_id)
                    VALUES (:usuario_id)
                """),
                {"usuario_id": usuario_id}
            )

        return jsonify({
            "status": 201,
            "message": "Usuario creado y vinculado a deportista",
            "data": {
                "usuario_id": usuario_id,
                "nameuser": nameuser,
                "email": email
            }
        }), 201

    except Exception as e:
        print("❌ ERROR al registrar usuario:", e)
        return jsonify({"error": str(e)}), 500




