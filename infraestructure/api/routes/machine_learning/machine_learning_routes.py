from flask import Blueprint, jsonify
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError, OperationalError

from infraestructure.api.routes.machine_learning.metrics_predictor import predict_future_metric
from infraestructure.config.config_bd import engine


machine_learning_bp = Blueprint(
    "machine_learning_bp",
    __name__,
    url_prefix="/api/machine_learning"
)


@machine_learning_bp.route(
    "/machine_learning_calories/<int:deportista_id>",
    methods=["GET"]
)
def get_machine_learning_calories(deportista_id):
    try:
        with engine.connect() as connectionBD:
            results = connectionBD.execute(
                text("""
                    SELECT fecha, calorias
                    FROM metricas_deportivas
                    WHERE deportista_id = :deportista_id
                    ORDER BY fecha ASC
                """),
                {"deportista_id": deportista_id}
            ).mappings().all()

            # Validación mínima de datos
            if not results or len(results) <= 50:
                return jsonify({
                    "status": 200,
                    "message": "No hay métricas suficientes para entrenar el modelo",
                    "predictions": []
                }), 200

            # Datos limpios para el modelo
            data = [
                {
                    "fecha": row["fecha"],
                    "calorias": row["calorias"]
                }
                for row in results
                if row["calorias"] is not None
            ]

            # Llamada al modelo ML
            predictions = predict_future_metric(
                data,
                "calorias",
                days_to_predict=7
            )

            return jsonify({
                "status": 200,
                "message": "Predicción generada correctamente",
                "predictions": predictions
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


@machine_learning_bp.route(
    "/machine_learning_velocidad_media/<int:deportista_id>",
    methods=["GET"]
)
def get_machine_learning_velocidad_media(deportista_id):
    try:
        with engine.connect() as connectionBD:
            results = connectionBD.execute(
                text("""
                    SELECT fecha, velocidad_media
                    FROM metricas_deportivas
                    WHERE deportista_id = :deportista_id
                    ORDER BY fecha ASC
                """),
                {"deportista_id": deportista_id}
            ).mappings().all()

            # Validación mínima de datos
            if not results or len(results) <= 50:
                return jsonify({
                    "status": 200,
                    "message": "No hay métricas suficientes para entrenar el modelo",
                    "predictions": []
                }), 200

            # Datos limpios para el modelo
            data = [
                {
                    "fecha": row["fecha"],
                    "velocidad_media": row["velocidad_media"]
                }
                for row in results
                if row["velocidad_media"] is not None
            ]

            # Llamada al modelo ML
            predictions = predict_future_metric(
                data,
                "velocidad_media",
                days_to_predict=7
            )

            return jsonify({
                "status": 200,
                "message": "Predicción generada correctamente",
                "predictions": predictions
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

##Frecuencia cardiaca predicciones

@machine_learning_bp.route(
    "/machine_learning_frecuencia_cardiaca/<int:deportista_id>",
    methods=["GET"]
)
def get_machine_learning_frecuencia_cardiaca(deportista_id):
    try:
        with engine.connect() as connectionBD:
            results = connectionBD.execute(
                text("""
                    SELECT fecha, frecuencia_cardiaca
                    FROM metricas_deportivas
                    WHERE deportista_id = :deportista_id
                    ORDER BY fecha ASC
                """),
                {"deportista_id": deportista_id}
            ).mappings().all()

            # Validación mínima de datos
            if not results or len(results) <= 50:
                return jsonify({
                    "status": 200,
                    "message": "No hay métricas suficientes para entrenar el modelo",
                    "predictions": []
                }), 200

            # Datos limpios para el modelo
            data = [
                {
                    "fecha": row["fecha"],
                    "frecuencia_cardiaca": row["frecuencia_cardiaca"]
                }
                for row in results
                if row["frecuencia_cardiaca"] is not None
            ]

            # Llamada al modelo ML
            predictions = predict_future_metric(
                data,
                "frecuencia_cardiaca",
                days_to_predict=7
            )

            return jsonify({
                "status": 200,
                "message": "Predicción generada correctamente",
                "predictions": predictions
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