from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.engine import row
from sqlalchemy.exc import SQLAlchemyError

from domain.entities.sportsperson.sportsperson import Sportsperson
from infraestructure.config.config_bd import engine

sport_bp = Blueprint("sport_bp", __name__, url_prefix="/api/sport")

## Obtener un deportista por su id
from flask import jsonify
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

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
                "deportistas": [
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

## Mostrar todos los deportistas


## Modificar datos de un deportista
