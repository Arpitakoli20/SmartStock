from fastapi import FastAPI, HTTPException
from sqlalchemy import select

from backend.database import engine, Medicine, Inventory, Consumption, Supplier


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
# LOW STOCK INVENTORY
# IMPORTANT: This route must come BEFORE
# /inventory/{medicine_id}
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


# --------------------------------------------------
# SINGLE MEDICINE INVENTORY
# IMPORTANT: This dynamic route comes AFTER
# /inventory/low-stock
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
# ALL CONSUMPTION
# --------------------------------------------------

@app.get("/consumption")
def get_consumption():

    with engine.connect() as connection:

        consumption = connection.execute(
            select(Consumption)
        ).fetchall()

        return [
            {
                "id": record.id,
                "date": record.date,
                "medicine_id": record.medicine_id,
                "quantity_consumed": record.quantity_consumed,
                "demand_type": record.demand_type
            }
            for record in consumption
        ]


# --------------------------------------------------
# MEDICINE-WISE CONSUMPTION
# --------------------------------------------------

@app.get("/consumption/{medicine_id}")
def get_medicine_consumption(medicine_id: str):

    with engine.connect() as connection:

        consumption = connection.execute(
            select(Consumption).where(
                Consumption.medicine_id == medicine_id
            )
        ).fetchall()

        if not consumption:
            raise HTTPException(
                status_code=404,
                detail="Medicine consumption data not found"
            )

        return [
            {
                "id": record.id,
                "date": record.date,
                "medicine_id": record.medicine_id,
                "quantity_consumed": record.quantity_consumed,
                "demand_type": record.demand_type
            }
            for record in consumption
        ]


# --------------------------------------------------
# ALL SUPPLIERS
# --------------------------------------------------

@app.get("/suppliers")
def get_suppliers():

    with engine.connect() as connection:

        suppliers = connection.execute(
            select(Supplier)
        ).fetchall()

        return [
            {
                "supplier_id": record.supplier_id,
                "supplier_name": record.supplier_name,
                "contact_email": record.contact_email,
                "lead_time_days": record.lead_time_days,
                "reliability_score": record.reliability_score,
                "location": record.location
            }
            for record in suppliers
        ]


# --------------------------------------------------
# SINGLE SUPPLIER
# --------------------------------------------------

@app.get("/suppliers/{supplier_id}")
def get_supplier(supplier_id: str):

    with engine.connect() as connection:

        supplier = connection.execute(
            select(Supplier).where(
                Supplier.supplier_id == supplier_id
            )
        ).first()

        if supplier is None:
            raise HTTPException(
                status_code=404,
                detail="Supplier not found"
            )

        return {
            "supplier_id": supplier.supplier_id,
            "supplier_name": supplier.supplier_name,
            "contact_email": supplier.contact_email,
            "lead_time_days": supplier.lead_time_days,
            "reliability_score": supplier.reliability_score,
            "location": supplier.location
        }