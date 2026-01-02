from flask import Blueprint, request, jsonify
import pandas as pd

upload_bp = Blueprint("upload_file_bp", __name__, url_prefix="/api/upload-file")


@upload_bp.route("/uploadfile", methods=["POST"])
def upload_file():

    # 1️⃣ Validar que llega el fichero
    if 'file' not in request.files:
        return jsonify({
            "status": 400,
            "error": "No se ha enviado ningún archivo"
        }), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({
            "status": 400,
            "error": "Nombre de archivo vacío"
        }), 400

    try:
        # 2️⃣ Detectar tipo de fichero
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file, sep=';', encoding='utf-8')
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            return jsonify({
                "status": 400,
                "error": "Formato de archivo no soportado"
            }), 400

        # 3️⃣ Respuesta estructurada (preview)
        return jsonify({
            "status": 200,
            "message": "Archivo leído correctamente",
            "filename": file.filename,
            "total_rows": len(df),
            "columns": df.columns.tolist(),
            "rows": df.head(10).to_dict(orient="records")
        }), 200

    except Exception as e:
        print("❌ ERROR UPLOAD FILE:", e)
        return jsonify({
            "status": 500,
            "error": "Error al procesar el archivo",
            "detail": str(e)
        }), 500
