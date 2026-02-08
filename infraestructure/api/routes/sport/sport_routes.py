from flask import Blueprint, jsonify, request
from domain.entities.sportsperson.sportsperson import Sportsperson
from infraestructure.config.config_bd import engine
from flask import jsonify
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

sport_bp = Blueprint("sport_bp", __name__, url_prefix="/api/sport")


##Obtener todos los deportistas
@sport_bp.route("/getAllSport", methods=["GET"])
def get_all_sport():
    try:
        with engine.connect() as connectionBD:
            deportistas = connectionBD.execute(
                text("SELECT * FROM deportistas")
            ).mappings().all()

            sportspersonList = [
                Sportsperson(
                    id=row["id"],
                    usuario_id=row["usuario_id"],
                    nombre=row["nombre"],
                    edad=row["edad"],
                    disciplina_deportiva=row["disciplina_deportiva"],
                    nacionalidad=row["nacionalidad"],
                    telefono=row["telefono"]
                )
                for row in deportistas
            ]

            return jsonify({
                "status": 200,
                "message": "Deportistas obtenidos correctamente",
                "data": [
                    {
                        "id": d.id,
                        "usuario_id": d.usuario_id,
                        "nombre": d.nombre,
                        "edad": d.edad,
                        "disciplina_deportiva": d.disciplina_deportiva,
                        "nacionalidad": d.nacionalidad,
                        "telefono": d.telefono
                    }
                    for d in sportspersonList
                ]
            }), 200

    except OperationalError:
        return jsonify({
            "status": 503,
            "error": "Base de datos no disponible"
        }), 503

    except SQLAlchemyError:
        return jsonify({
            "status": 500,
            "error": "Error ejecutando la consulta"
        }), 500

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": "Error interno del servidor",
            "detail": str(e)
        }), 500


## Obtener un deportista por su id
@sport_bp.route("/getSportById/<int:id>", methods=["GET"])
def get_sport_by_id(id):
    try:
        with engine.connect() as connectionBD:
            existing_deportista = connectionBD.execute(
                text("SELECT * FROM deportistas WHERE id = :id"),
                {"id": id}
            ).mappings().first()

            if not existing_deportista:
                return jsonify({
                    "status": 404,
                    "error": "Deportista no encontrado"
                }), 404

            deportista = Sportsperson(
                id=existing_deportista["id"],
                usuario_id=existing_deportista["usuario_id"],
                nombre=existing_deportista["nombre"],
                edad=existing_deportista["edad"],
                disciplina_deportiva=existing_deportista["disciplina_deportiva"],
                nacionalidad=existing_deportista["nacionalidad"],
                telefono=existing_deportista["telefono"]
            )

        return jsonify({
            "status": 200,
            "message": "Deportista encontrado",
            "data": {
                "id": deportista.id,
                "usuario_id": deportista.usuario_id,
                "nombre": deportista.nombre,
                "edad": deportista.edad,
                "disciplina_deportiva": deportista.disciplina_deportiva,
                "nacionalidad": deportista.nacionalidad,
                "telefono": deportista.telefono
            }
        }), 200

    except OperationalError:
        return jsonify({
            "status": 503,
            "error": "Base de datos no disponible"
        }), 503

    except SQLAlchemyError:
        return jsonify({
            "status": 500,
            "error": "Error ejecutando la consulta"
        }), 500

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": "Error interno del servidor",
            "detail": str(e)
        }), 500


## Actualiza un deportista por su id(Solo lo podran modificarl los que tenga el rol de admin)
@sport_bp.route("/updateSportById/<int:id>", methods=["PUT"])
def update_sport_by_id(id):
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "status": 400,
                "error": "No se enviaron datos para actualizar"
            }), 400

        with engine.connect() as connectionBD:
            # 1️⃣ Comprobar si existe
            existing = connectionBD.execute(
                text("SELECT id FROM deportistas WHERE id = :id"),
                {"id": id}
            ).fetchone()

            if not existing:
                return jsonify({
                    "status": 404,
                    "error": "Deportista no encontrado"
                }), 404

            # 2️⃣ Actualizar (PATCH-like con COALESCE)
            connectionBD.execute(
                text("""
                    UPDATE deportistas
                    SET
                        usuario_id = COALESCE(:usuario_id, usuario_id),
                        nombre = COALESCE(:nombre, nombre),
                        edad = COALESCE(:edad, edad),
                        disciplina_deportiva = COALESCE(:disciplina_deportiva, disciplina_deportiva),
                        nacionalidad = COALESCE(:nacionalidad, nacionalidad),
                        telefono = COALESCE(:telefono, telefono)
                    WHERE id = :id
                """),
                {
                    "id": id,
                    "usuario_id": data.get("usuario_id"),
                    "nombre": data.get("nombre"),
                    "edad": data.get("edad"),
                    "disciplina_deportiva": data.get("disciplina_deportiva"),
                    "nacionalidad": data.get("nacionalidad"),
                    "telefono": data.get("telefono")
                }
            )

            connectionBD.commit()

        return jsonify({
            "status": 200,
            "message": "Deportista actualizado correctamente"
        }), 200

    except OperationalError:
        return jsonify({
            "status": 503,
            "error": "Base de datos no disponible"
        }), 503

    except SQLAlchemyError:
        return jsonify({
            "status": 500,
            "error": "Error ejecutando la actualización"
        }), 500

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": "Error interno del servidor",
            "detail": str(e)
        }), 500

##Obtener informacion de un usuario por su id_usuario
@sport_bp.route("/getInfoSport/<int:usuario_id>", methods=["GET"])
def getsportInfo(usuario_id):
    try:
        with engine.connect() as connectionBD:
            existing_deportista = connectionBD.execute(
                text("SELECT * FROM deportistas WHERE usuario_id = :usuario_id"),
                {"usuario_id": usuario_id}
            ).mappings().first()

            if not existing_deportista:
                return jsonify({
                    "status": 404,
                    "error": "El deportista no existe en nuestra base de datos"
                }), 404

            deportista = Sportsperson(
                id=existing_deportista["id"],
                usuario_id=existing_deportista["usuario_id"],
                nombre=existing_deportista["nombre"],
                edad=existing_deportista["edad"],
                disciplina_deportiva=existing_deportista["disciplina_deportiva"],
                nacionalidad=existing_deportista["nacionalidad"],
                telefono=existing_deportista["telefono"]
            )

        return jsonify({
            "status": 200,
            "message": "Deportista encontrado",
            "data": {
                "id": deportista.id,
                "usuario_id": deportista.usuario_id,
                "nombre": deportista.nombre,
                "edad": deportista.edad,
                "disciplina_deportiva": deportista.disciplina_deportiva,
                "nacionalidad": deportista.nacionalidad,
                "telefono": deportista.telefono
            }
        }), 200

    except OperationalError:
        return jsonify({
            "status": 503,
            "error": "Base de datos no disponible"
        }), 503

    except SQLAlchemyError:
        return jsonify({
            "status": 500,
            "error": "Error ejecutando la consulta"
        }), 500

    except Exception as e:
        return jsonify({
            "status": 500,
            "error": "Error interno del servidor",
            "detail": str(e)
        }), 500