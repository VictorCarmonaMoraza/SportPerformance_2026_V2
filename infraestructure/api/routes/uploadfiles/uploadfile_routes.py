from flask import Blueprint, request, jsonify
import pandas as pd
from sqlalchemy import text

from infraestructure.config.config_bd import engine

upload_bp = Blueprint("upload_file_bp", __name__, url_prefix="/api/upload-file")


@upload_bp.route("/uploadfile", methods=["POST"])
def upload_file():

    if 'file' not in request.files:
        return jsonify({"status": 400, "error": "No se ha enviado ningún archivo"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"status": 400, "error": "Nombre de archivo vacío"}), 400

    deportista_id = request.form.get('deportista_id')
    if not deportista_id:
        return jsonify({"status": 400, "error": "No se ha enviado el deportista_id"}), 400

    try:
        deportista_id = int(deportista_id)
    except ValueError:
        return jsonify({"status": 400, "error": "deportista_id inválido"}), 400

    try:
        # ===============================
        # 1️⃣ LEER FICHERO
        # ===============================
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file, sep=';', encoding='utf-8')
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return jsonify({"status": 400, "error": "Formato no soportado"}), 400

        # Normalizamos columnas
        df.columns = df.columns.str.lower().str.strip()

        required_columns = {'fecha'}
        if not required_columns.issubset(df.columns):
            return jsonify({
                "status": 400,
                "error": "El fichero debe contener la columna 'fecha'"
            }), 400

        inserted = 0
        updated = 0

        # ===============================
        # 2️⃣ TRANSACCIÓN
        # ===============================
        with engine.begin() as conn:

            for _, row in df.iterrows():

                fecha = pd.to_datetime(row['fecha']).date()

                # ¿Existe ya la métrica?
                exists = conn.execute(
                    text("""
                        SELECT id
                        FROM metricas_deportivas
                        WHERE deportista_id = :deportista_id
                          AND fecha = :fecha
                    """),
                    {
                        "deportista_id": deportista_id,
                        "fecha": fecha
                    }
                ).fetchone()

                values = {
                    "deportista_id": deportista_id,
                    "fecha": fecha,
                    "peso": row.get("peso"),
                    "altura": row.get("altura"),
                    "frecuencia_cardiaca": row.get("frecuencia_cardiaca"),
                    "velocidad_media": row.get("velocidad_media"),
                    "distancia": row.get("distancia"),
                    "calorias": row.get("calorias"),
                    "duracion_min": row.get("duracion_min"),
                    "fc_media": row.get("fc_media"),
                    "fc_max": row.get("fc_max"),
                    "ritmo_medio": row.get("ritmo_medio"),
                    "rpe": row.get("rpe"),
                }

                if exists:
                    # ===============================
                    # UPDATE
                    # ===============================
                    conn.execute(
                        text("""
                            UPDATE metricas_deportivas
                            SET peso = :peso,
                                altura = :altura,
                                frecuencia_cardiaca = :frecuencia_cardiaca,
                                velocidad_media = :velocidad_media,
                                distancia = :distancia,
                                calorias = :calorias,
                                duracion_min = :duracion_min,
                                fc_media = :fc_media,
                                fc_max = :fc_max,
                                ritmo_medio = :ritmo_medio,
                                rpe = :rpe
                            WHERE deportista_id = :deportista_id
                              AND fecha = :fecha
                        """),
                        values
                    )
                    updated += 1
                else:
                    # ===============================
                    # INSERT
                    # ===============================
                    conn.execute(
                        text("""
                            INSERT INTO metricas_deportivas (
                                deportista_id, fecha, peso, altura,
                                frecuencia_cardiaca, velocidad_media,
                                distancia, calorias, duracion_min,
                                fc_media, fc_max, ritmo_medio, rpe
                            )
                            VALUES (
                                :deportista_id, :fecha, :peso, :altura,
                                :frecuencia_cardiaca, :velocidad_media,
                                :distancia, :calorias, :duracion_min,
                                :fc_media, :fc_max, :ritmo_medio, :rpe
                            )
                        """),
                        values
                    )
                    inserted += 1

        # ===============================
        # 3️⃣ RESPUESTA FINAL
        # ===============================
        return jsonify({
            "status": 200,
            "message": "Importación completada",
            "total_rows": len(df),
            "inserted": inserted,
            "updated": updated
        }), 200

    except Exception as e:
        print("❌ ERROR IMPORT:", e)
        return jsonify({
            "status": 500,
            "error": "Error al importar métricas",
            "detail": str(e)
        }), 500

