import csv
from datetime import date
from pathlib import Path

from database import engine, Medicine, Supplier, Inventory


# Project folders
BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BACKEND_DIR.parent
DATA_DIR = PROJECT_DIR / "data"


def read_csv(filename):
    file_path = DATA_DIR / filename

    with open(file_path, "r", encoding="utf-8-sig", newline="") as file:
        return list(csv.DictReader(file))


def to_date(value):
    if not value:
        return None
    return date.fromisoformat(value)


def load_medicines():
    rows = read_csv("medicines.csv")

    with engine.begin() as connection:
        for row in rows:
            connection.execute(
                Medicine.__table__.insert().prefix_with("OR REPLACE"),
                {
                    "medicine_id": row["medicine_id"],
                    "medicine_name": row["medicine_name"],
                    "category": row["category"],
                    "unit": row["unit"],
                    "unit_price": float(row["unit_price"]),
                    "criticality": row["criticality"],
                },
            )

    print(f"Medicines loaded: {len(rows)}")


def load_suppliers():
    rows = read_csv("suppliers.csv")

    with engine.begin() as connection:
        for row in rows:
            connection.execute(
                Supplier.__table__.insert().prefix_with("OR REPLACE"),
                {
                    "supplier_id": row["supplier_id"],
                    "supplier_name": row["supplier_name"],
                    "contact_email": row["contact_email"],
                    "lead_time_days": int(row["lead_time_days"]),
                    "reliability_score": float(row["reliability_score"]),
                    "location": row["location"],
                },
            )

    print(f"Suppliers loaded: {len(rows)}")


def load_inventory():
    rows = read_csv("inventory.csv")

    with engine.begin() as connection:
        for row in rows:
            connection.execute(
                Inventory.__table__.insert().prefix_with("OR REPLACE"),
                {
                    "medicine_id": row["medicine_id"],
                    "current_stock": int(row["current_stock"]),
                    "reorder_level": int(row["reorder_level"]),
                    "safety_stock": int(row["safety_stock"]),
                    "expiry_date": to_date(row["expiry_date"]),
                    "supplier_id": row["supplier_id"],
                    "last_restock_date": to_date(row["last_restock_date"]),
                },
            )

    print(f"Inventory records loaded: {len(rows)}")


if __name__ == "__main__":
    load_medicines()
    load_suppliers()
    load_inventory()

    print("All CSV data loaded successfully!")