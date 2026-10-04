from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from backend.database import engine, Medicine, Inventory

app = FastAPI(
    title="SmartStock API",
    description="Backend API for SmartStock medicine inventory system",
    version="1.0.0"
)


# --------------------------------------------------
# HOME
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "SmartStock API is running"
    }


# --------------------------------------------------
# MEDICINES
# --------------------------------------------------

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


# --------------------------------------------------
# ALL INVENTORY
# --------------------------------------------------

@app.get("/inventory")
def get_inventory():

    with engine.connect() as connection:

        inventory = connection.execute(
            select(Inventory)
        ).fetchall()

        return [
            {
                "medicine_id": item.medicine_id,
                "current_stock": item.current_stock,
                "reorder_level": item.reorder_level,
                "safety_stock": item.safety_stock,
                "expiry_date": item.expiry_date,
                "supplier_id": item.supplier_id,
                "last_restock_date": item.last_restock_date
            }
            for item in inventory
        ]


# --------------------------------------------------
# SINGLE MEDICINE INVENTORY
# --------------------------------------------------

@app.get("/inventory/{medicine_id}")
def get_medicine_inventory(medicine_id: str):

    with engine.connect() as connection:

        item = connection.execute(
            select(Inventory).where(
                Inventory.medicine_id == medicine_id
            )
        ).first()

        if item is None:
            raise HTTPException(
                status_code=404,
                detail="Medicine not found"
            )

        return {
            "medicine_id": item.medicine_id,
            "current_stock": item.current_stock,
            "reorder_level": item.reorder_level,
            "safety_stock": item.safety_stock,
            "expiry_date": item.expiry_date,
            "supplier_id": item.supplier_id,
            "last_restock_date": item.last_restock_date
        }


# --------------------------------------------------
# LOW STOCK MEDICINES
# --------------------------------------------------

@app.get("/inventory/low-stock")
def get_low_stock():

    with engine.connect() as connection:

        inventory = connection.execute(
            select(Inventory).where(
                Inventory.current_stock <= Inventory.reorder_level
            )
        ).fetchall()

        return [
            {
                "medicine_id": item.medicine_id,
                "current_stock": item.current_stock,
                "reorder_level": item.reorder_level,
                "safety_stock": item.safety_stock,
                "supplier_id": item.supplier_id
            }
            for item in inventory
        ]