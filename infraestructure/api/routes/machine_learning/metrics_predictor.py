import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import timedelta


def predict_future_metric(metrics, value_key, days_to_predict=7):
    """
    metrics: lista de dicts -> [{fecha, calorias, velocidad_media, ...}]
    value_key: str -> nombre del campo a predecir
    days_to_predict: número de días a predecir
    """

    # -------------------------
    # 1. DataFrame
    # -------------------------
    df = pd.DataFrame(metrics)

    if df.empty or value_key not in df.columns:
        return []

    df["fecha"] = pd.to_datetime(df["fecha"])
    df = df.sort_values("fecha")

    # -------------------------
    # 2. Rellenar fechas faltantes
    # -------------------------
    df = df.set_index("fecha")

    full_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq="D"
    )

    df = df.reindex(full_range)

    # -------------------------
    # 3. Limpiar nulos
    # -------------------------
    df[value_key] = df[value_key].interpolate(method="linear")
    df = df.dropna(subset=[value_key])

    if df.empty:
        return []

    # -------------------------
    # 4. Variable temporal
    # -------------------------
    df["t"] = np.arange(len(df))

    X = df[["t"]]
    y = df[value_key]

    # -------------------------
    # 5. Entrenar modelo
    # -------------------------
    model = LinearRegression()
    model.fit(X, y)

    # -------------------------
    # 6. Predicción futura
    # -------------------------
    last_t = df["t"].iloc[-1]

    future_t = np.arange(
        last_t + 1,
        last_t + 1 + days_to_predict
    ).reshape(-1, 1)

    predictions = model.predict(future_t)

    future_dates = [
        df.index.max() + timedelta(days=i)
        for i in range(1, days_to_predict + 1)
    ]

    return [
        {
            "fecha": future_dates[i].strftime("%Y-%m-%d"),
            "predicciones": round(float(predictions[i]), 2)
        }
        for i in range(days_to_predict)
    ]
