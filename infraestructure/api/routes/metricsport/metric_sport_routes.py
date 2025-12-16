from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from domain.entities.metricsperson.metricsperson import Metricsperson
from infraestructure.config.config_bd import engine

metrics_person_bp = Blueprint("metrics_person_bp", __name__, url_prefix="/api/metrics")

##Obtener metricas de un deportista por su id
@metrics_person_bp.route("/metricsPersonById/<int:deportista_id>", methods=["GET"])
def get_metrics_person(deportista_id):
    try:
        with engine.connect() as connectionBD:
            existing_metrics = connectionBD.execute(
                text("SELECT * FROM metricas_deportivas WHERE deportista_id = :deportista_id"),
                {"deportista_id":deportista_id}
            ).mappings().all()

            if not existing_metrics:
                return jsonify({
                    "status": 200,
                    "message": "No existen métricas para este deportista",
                    "metrics": []
                }), 200

            metrics = [
                Metricsperson(
                    id=row["id"],
                    deportista_id=row["deportista_id"],
                    fecha=row["fecha"],
                    peso=row["peso"],
                    altura=row["altura"],
                    frecuencia_cardiaca=row["frecuencia_cardiaca"],
                    velocidad_media=row["velocidad_media"],
                    distancia=row["distancia"],
                    calorias=row["calorias"]
                )
                for row in existing_metrics
            ]

            return jsonify({
                "status": 200,
                "message": "Métricas obtenidas correctamente",
                "metrics": [
                    {
                        "id": m.id,
                        "deportista_id": m.deportista_id,
                        "fecha": m.fecha,
                        "peso": m.peso,
                        "altura": m.altura,
                        "frecuencia_cardiaca": m.frecuencia_cardiaca,
                        "velocidad_media": m.velocidad_media,
                        "distancia": m.distancia,
                        "calorias": m.calorias
                    }
                    for m in metrics
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
