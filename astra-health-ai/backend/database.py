
import sqlite3
from pathlib import Path

# Ubicación de la base de datos
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "astra_health.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


# Crear tabla de mediciones
def init_db():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS health_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            astronaut_id TEXT NOT NULL,
            heart_rate INTEGER NOT NULL,
            oxygen_saturation INTEGER NOT NULL,
            sleep_hours REAL NOT NULL,
            activity INTEGER NOT NULL,
            data_type TEXT DEFAULT 'simulated',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# Guardar mediciones
def save_health_data(data):
    connection = get_connection()

    connection.execute("""
        INSERT INTO health_measurements (
            astronaut_id,
            heart_rate,
            oxygen_saturation,
            sleep_hours,
            activity,
            data_type
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        data["astronaut_id"],
        data["heart_rate"],
        data["oxygen_saturation"],
        data["sleep_hours"],
        data["activity"],
        data.get("data_type", "simulated")
    ))

    connection.commit()
    connection.close()


# Consultar historial
def get_health_history(limit=50):
    connection = get_connection()

    cursor = connection.execute("""
        SELECT * FROM health_measurements
        ORDER BY created_at DESC, id DESC
        LIMIT ?
    """, (limit,))

    results = [dict(row) for row in cursor.fetchall()]

    connection.close()
    return results
