
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# Indicadores que analizará el modelo
FEATURES = [
    "heart_rate",
    "oxygen_saturation",
    "sleep_hours",
    "activity"
]

MIN_TRAINING_SAMPLES = 20


def prepare_data(measurements):
    """Extrae y valida los indicadores de las mediciones."""

    data = []

    for measurement in measurements:
        try:
            values = [
                float(measurement[feature])
                for feature in FEATURES
            ]

            if np.all(np.isfinite(values)):
                data.append(values)

        except (KeyError, TypeError, ValueError):
            continue

    return np.array(data, dtype=float)


def train_model(measurements):
    """Entrena Isolation Forest con el historial disponible."""

    data = prepare_data(measurements)

    if len(data) < MIN_TRAINING_SAMPLES:
        raise ValueError(
            f"Se necesitan al menos {MIN_TRAINING_SAMPLES} "
            f"mediciones válidas. Disponibles: {len(data)}."
        )

    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)

    model = IsolationForest(
        n_estimators=200,
        contamination="auto",
        random_state=42
    )

    model.fit(scaled_data)

    return {
        "model": model,
        "scaler": scaler,
        "training_samples": len(data)
    }


def analyze_measurement(model_bundle, measurement):
    """Analiza una nueva medición frente al patrón aprendido."""

    values = prepare_data([measurement])

    if len(values) == 0:
        raise ValueError("La medición contiene datos inválidos.")

    model = model_bundle["model"]
    scaler = model_bundle["scaler"]

    scaled_values = scaler.transform(values)

    prediction = int(model.predict(scaled_values)[0])
    anomaly_score = float(
        model.score_samples(scaled_values)[0]
    )

    # Identificar qué indicadores se alejan más
    # del promedio del conjunto de entrenamiento.
    deviations = np.abs(scaled_values[0])

    indicator_deviations = {
        feature: round(float(deviation), 3)
        for feature, deviation in zip(FEATURES, deviations)
    }

    most_unusual_indicators = sorted(
        indicator_deviations,
        key=indicator_deviations.get,
        reverse=True
    )[:2]

    return {
        "is_anomaly": prediction == -1,
        "classification": (
            "unusual_measurement"
            if prediction == -1
            else "usual_measurement"
        ),
        "anomaly_score": round(anomaly_score, 4),
        "indicator_deviations": indicator_deviations,
        "most_unusual_indicators": most_unusual_indicators,
        "training_samples": model_bundle["training_samples"],
        "message": (
            "La medición se aparta del patrón aprendido."
            if prediction == -1
            else "La medición no fue identificada como inusual."
        ),
        "disclaimer": (
            "Resultado experimental. No constituye un "
            "diagnóstico ni una evaluación clínica de riesgo."
        )
    }
