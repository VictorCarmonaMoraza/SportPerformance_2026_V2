from calendar import monthrange
from datetime import date

from dateutil.relativedelta import relativedelta
from flask import Blueprint, jsonify, request
from sqlalchemy import text
from sqlalchemy.exc import OperationalError, SQLAlchemyError

from domain.entities.metricsperson.metricsperson import Metricsperson
from infraestructure.config.config_bd import engine
from infraestructure.helpers.helpers import getFechas, getLastYear

metrics_person_bp = Blueprint("metrics_person_bp", __name__, url_prefix="/api/metrics")


##Obtener metricas de un deportista por su id
@metrics_person_bp.route("/metricsPersonById/<int:deportista_id>", methods=["GET"])
def get_metrics_person(deportista_id):
    try:
        with engine.connect() as connectionBD:
            existing_metrics = connectionBD.execute(
                text("SELECT * FROM metricas_deportivas WHERE deportista_id = :deportista_id"),
                {"deportista_id": deportista_id}
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


# Obtener metricas por rango de fechas(fecha inicial, fecha final y deportista_id)
@metrics_person_bp.route("/getByDateRange/<int:deportista_id>", methods=["GET"])
def get_metrics_by_date_range(deportista_id: int):
    fecha_inicio: str = request.args.get("fecha_inicio")
    fecha_fin: str = request.args.get("fecha_fin")

    if not fecha_inicio or not fecha_fin:
        return jsonify({
            "status": 400,
            "error": "Los parámetros fecha_inicio y fecha_fin son obligatorios"
        }), 400

    try:
        with engine.connect() as connectionBD:
            existing_metrics = connectionBD.execute(
                text("""
                    SELECT *
                    FROM metricas_deportivas
                    WHERE deportista_id = :deportista_id
                      AND fecha BETWEEN :fecha_inicio AND :fecha_fin
                    ORDER BY fecha
                """),
                {
                    "deportista_id": deportista_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            ).mappings().all()

            if not existing_metrics:
                return jsonify({
                    "status": 200,
                    "message": "No existen metricas para ese rango de fechas",
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


##Obtener metricas del ultimo año(fecha actual-menos 365 dias)
@metrics_person_bp.route("/lastYear/<int:deportista_id>", methods=["GET"])
def get_metrics_last_year(deportista_id: int):
    fecha_fin: date = date.today()
    fecha_inicio: date = fecha_fin - relativedelta(years=1)

    if fecha_inicio > fecha_fin:
        return jsonify({
            "status": 400,
            "error": "La fecha inicial no puede ser mayor que la fecha final"
        }), 400

    try:
        with engine.connect() as connectionBD:
            metrics = connectionBD.execute(
                text("""
                    SELECT *
                    FROM metricas_deportivas
                    WHERE deportista_id = :deportista_id
                      AND fecha BETWEEN :fecha_inicio AND :fecha_fin
                    ORDER BY fecha
                """),
                {
                    "deportista_id": deportista_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            ).mappings().all()

            if not metrics:
                return jsonify({
                    "status": 200,
                    "message": "No existen metricas para ese rango de fechas",
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
                for row in metrics
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


# obtener metricas de un año concreto(pasarle solo el año y deportista_id)
@metrics_person_bp.route("/getMetricsByYear/<int:deportista_id>/<int:year>", methods=["GET"])
def getMetricsByYear(deportista_id, year):
    fecha_inicio, fecha_fin = getFechas(year)

    try:
        with engine.connect() as connectionBD:
            ##Comprobar que el usuario existe en base de datos
            existe_deportista = connectionBD.execute(
                text("""
                    SELECT 1
                    FROM deportistas
                    WHERE id = :deportista_id
                """),
                {"deportista_id": deportista_id}
            ).scalar()

            if not existe_deportista:
                return jsonify({
                    "status": 404,
                    "message": "El deportista no existe en la base de datos"
                }), 404

            metrics = connectionBD.execute(
                text("""SELECT *
                    FROM metricas_deportivas
                    WHERE deportista_id=:deportista_id
                      AND fecha>=:fecha_inicio
                      AND fecha<:fecha_fin
                    ORDER BY fecha"""
                     ),
                {
                    "deportista_id": deportista_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            ).mappings().all()

            ##Mapear los campos contra el modelo
            if not metrics:
                return jsonify({
                    "status": 200,
                    "message": "No existen metricas para ese año",
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
                for row in metrics
            ]

            return jsonify({
                "status": 200,
                "message": "Métricas obtenidas correctamente",
                "metrics": [
                    {
                        "id": m.id,
                        "deportista_id": m.deportista_id,
                        "fecha": m.fecha.strftime("%Y/%m/%d"),
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


##Obtener metricas del ultimo año(fecha actual-menos 365 dias)
@metrics_person_bp.route("/getlastYearMetrics/<int:deportista_id>", methods=["GET"])
def getlastYearMetrics(deportista_id: int):
    n_dias =365
    fecha_actual = date.today()
    fecha_inicio, fecha_fin = getLastYear(fecha_actual,n_dias)

    # Abrimos conexion
    try:
        with engine.connect() as connectionBD:
            metrics = connectionBD.execute(
                text("""
                    SELECT *
                    FROM metricas_deportivas
                    WHERE deportista_id = :deportista_id
                      AND fecha >= :fecha_inicio
                      AND fecha <= :fecha_fin
                    ORDER BY fecha
                    """),
                {
                    "deportista_id": deportista_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            ).mappings().all()

            if not metrics:
                return jsonify({
                    "status": 404,
                    "message": "No existen metricas durante el ultimo año"
                }), 404

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
                for row in metrics
            ]

            return jsonify({
                "status": 200,
                "message": "Métricas obtenidas correctamente",
                "numero_registros": len(metrics),
                "metrics": [
                    {
                        "id": m.id,
                        "deportista_id": m.deportista_id,
                        "fecha": m.fecha.strftime("%Y/%m/%d"),
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


# Obtener metricas de los ultimos 7 dias(fecha actual- 7 dias atras y deportista_id)
@metrics_person_bp.route("/getlastWeek/<int:deportista_id>", methods=["GET"])
def getLastWeek(deportista_id: int):
    n_dias = 7
    fecha_actual =date.today()
    fecha_inicio, fecha_fin = getLastYear(fecha_actual,n_dias)

    ##Abrimos conexion
    try:
        with engine.connect() as connectionBD:
            metrics = connectionBD.execute(
                text("""
                        SELECT *
                        FROM metricas_deportivas
                        WHERE deportista_id = :deportista_id
                          AND fecha >= :fecha_inicio
                          AND fecha <= :fecha_fin
                        ORDER BY fecha
                        """),
                {
                    "deportista_id": deportista_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            ).mappings().all()

            if not metrics:
                return jsonify({
                    "status": 404,
                    "message": "No existen metricas durante la ultima semana"
                }), 404

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
                for row in metrics
            ]

            return jsonify({
                "status": 200,
                "message": "Métricas obtenidas correctamente",
                "numero_registros": len(metrics),
                "metrics": [
                    {
                        "id": m.id,
                        "deportista_id": m.deportista_id,
                        "fecha": m.fecha.strftime("%Y/%m/%d"),
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


# obtener metricas de un mes concreto(pasarle mes y deportista_id)
@metrics_person_bp.route("/getMonthMetrics/<int:deportista_id>/<int:month>", methods=["GET"])
def getMetricsMonth(deportista_id: int, month: int):

    # Validar mes
    if month < 1 or month > 12:
        return jsonify({
            "status": 400,
            "message": "El mes debe estar entre 1 y 12"
        }), 400

    # Año actual
    year = date.today().year

    # Rango de fechas del mes
    fecha_inicio = date(year, month, 1)
    ultimo_dia = monthrange(year, month)[1]
    fecha_fin = date(year, month, ultimo_dia)

    try:
        with engine.connect() as connectionBD:

            # Comprobar que el deportista existe
            existe_deportista = connectionBD.execute(
                text("""
                    SELECT 1
                    FROM deportistas
                    WHERE id = :deportista_id
                """),
                {"deportista_id": deportista_id}
            ).scalar()

            if not existe_deportista:
                return jsonify({
                    "status": 404,
                    "message": "El deportista no existe en la base de datos"
                }), 404

            # Obtener métricas
            metrics = connectionBD.execute(
                text("""
                    SELECT *
                    FROM metricas_deportivas
                    WHERE deportista_id = :deportista_id
                      AND fecha >= :fecha_inicio
                      AND fecha <= :fecha_fin
                    ORDER BY fecha
                """),
                {
                    "deportista_id": deportista_id,
                    "fecha_inicio": fecha_inicio,
                    "fecha_fin": fecha_fin
                }
            ).mappings().all()

            if not metrics:
                return jsonify({
                    "status": 200,
                    "message": "No existen métricas para ese mes",
                    "numero_registros": 0,
                    "metrics": []
                }), 200

            # Mapear resultados
            return jsonify({
                "status": 200,
                "message": "Métricas obtenidas correctamente",
                "numero_registros": len(metrics),
                "metrics": [
                    {
                        "id": row["id"],
                        "deportista_id": row["deportista_id"],
                        "fecha": row["fecha"].strftime("%Y/%m/%d"),
                        "peso": row["peso"],
                        "altura": row["altura"],
                        "frecuencia_cardiaca": row["frecuencia_cardiaca"],
                        "velocidad_media": row["velocidad_media"],
                        "distancia": row["distancia"],
                        "calorias": row["calorias"]
                    }
                    for row in metrics
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

