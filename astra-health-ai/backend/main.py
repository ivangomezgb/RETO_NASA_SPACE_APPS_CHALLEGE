
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import random

from backend.database import (
    init_db,
    save_health_data,
    get_health_history
)

from ai.anomaly_detection import (
    train_model,
    analyze_measurement
)

app = FastAPI(
    title="ASTRA HEALTH AI",
    description="Space Health Monitoring System",
    version="1.2.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {
        "project": "ASTRA HEALTH AI",
        "status": "online",
        "message": "Space Health API operational"
    }


@app.get("/api/v1/health")
def health_status():

    measurement = {
        "astronaut_id": "ASTRONAUT-001",
        "heart_rate": random.randint(60, 104),
        "oxygen_saturation": random.randint(93, 99),
        "sleep_hours": round(random.uniform(3, 8), 1),
        "activity": random.randint(0, 100),
        "data_type": "simulated"
    }

    save_health_data(measurement)

    return measurement


@app.get("/api/v1/health/history")
def health_history():

    history = get_health_history(limit=1000)

    return {
        "astronaut_id": "ASTRONAUT-001",
        "total_measurements": len(history),
        "measurements": history
    }


# NUEVO: análisis mediante Machine Learning
@app.get("/api/v1/health/analyze")
def analyze_health():

    history = get_health_history(limit=1000)

    if len(history) < 21:
        raise HTTPException(
            status_code=400,
            detail="Se necesitan al menos 21 mediciones."
        )

    # El historial está ordenado de más reciente a más antiguo.
    # Entrenamos con las anteriores y analizamos la última.
    training_data = history[1:]
    latest_measurement = history[0]

    try:
        model_bundle = train_model(training_data)

        result = analyze_measurement(
            model_bundle,
            latest_measurement
        )

        return {
            "astronaut_id": latest_measurement["astronaut_id"],
            "analyzed_measurement_id": latest_measurement["id"],
            "model": "Isolation Forest",
            "analysis": result
        }

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
