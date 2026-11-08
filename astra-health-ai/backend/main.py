
from fastapi import FastAPI
import random
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="ASTRA HEALTH AI",
    description="Space Health Monitoring System",
    version="1.0.0"
)

# Permitir comunicación con nuestro frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Solo para desarrollo local
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "project": "ASTRA HEALTH AI",
        "status": "online",
        "message": "Space Health API operational"
    }

@app.get("/api/v1/health")
def health_status():

    return {
        "astronaut_id": "ASTRONAUT-001",
        "heart_rate": random.randint(60, 104),
        "oxygen_saturation": random.randint(93, 99),
        "sleep_hours": round(random.uniform(3, 8), 1),
        "activity": random.randint(0, 100),
        "data_type": "simulated"
    }