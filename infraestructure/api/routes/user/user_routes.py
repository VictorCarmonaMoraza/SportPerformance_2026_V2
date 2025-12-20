from flask import Blueprint, request, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, OperationalError
from infraestructure.config.config_bd import engine

user_bp = Blueprint("user_bp", __name__, url_prefix="/api/user")


@user_bp.route("/updateUser/<int:id>", methods=["PUT"])
def update_user_by_id(id):
    try:
        data = request.form.to_dict()
        file = request.files.get("foto")

        if not data and not file:
            return jsonify({
                "status": 400,
                "error": "No se enviaron datos para actualizar"
            }), 400

        foto_bytes = None
        foto_mime = None
        foto_nombre = None

        if file:
            foto_bytes = file.read()
            foto_mime = file.content_type
            foto_nombre = file.filename

        with engine.begin() as connectionBD:

            existing = connectionBD.execute(
                text("SELECT id FROM usuarios WHERE id = :id"),
                {"id": id}
            ).fetchone()

            if not existing:
                return jsonify({
                    "status": 404,
                    "error": "Usuario no encontrado"
                }), 404

            connectionBD.execute(
                text("""
                    UPDATE usuarios
                    SET
                        nameuser = COALESCE(:nameuser, nameuser),
                        email = COALESCE(:email, email),
                        foto = COALESCE(:foto, foto),
                        foto_mime = COALESCE(:foto_mime, foto_mime),
                        foto_nombre = COALESCE(:foto_nombre, foto_nombre)
                    WHERE id = :id
                """),
                {
                    "id": id,
                    "nameuser": data.get("nameuser"),
                    "email": data.get("email"),
                    "foto": foto_bytes,
                    "foto_mime": foto_mime,
                    "foto_nombre": foto_nombre
                }
            )

        return jsonify({
            "status": 200,
            "message": "Usuario actualizado correctamente"
        }), 200

    except OperationalError:
        return jsonify({
            "status": 503,
            "error": "Base de datos no disponible"
        }), 503

    except SQLAlchemyError as e:
        return jsonify({
            "status": 500,
            "error": "Error ejecutando la actualización",
            "detail": str(e)
        }), 500

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": "Error interno del servidor",
            "detail": str(e)
        }), 500
