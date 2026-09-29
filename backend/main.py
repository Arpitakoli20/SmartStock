from fastapi import FastAPI
from sqlalchemy import select

from database import engine, Medicine


app = FastAPI(
    title="SmartStock API",
    description="Backend API for SmartStock medicine inventory system",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "SmartStock API is running"
    }


@app.get("/medicines")
def get_medicines():
    with engine.connect() as connection:
        medicines = connection.execute(
            select(Medicine)
        ).fetchall()

        return [
            {
                "medicine_id": medicine.medicine_id,
                "medicine_name": medicine.medicine_name,
                "category": medicine.category,
                "unit": medicine.unit,
                "unit_price": medicine.unit_price,
                "criticality": medicine.criticality
            }
            for medicine in medicines
        ]