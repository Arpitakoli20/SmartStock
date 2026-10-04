import csv
from datetime import date
from pathlib import Path

from sqlalchemy.dialects.postgresql import insert

from backend.database import engine, Medicine, Supplier, Inventory


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

            statement = insert(Medicine).values(
                medicine_id=row["medicine_id"],
                medicine_name=row["medicine_name"],
                category=row["category"],
                unit=row["unit"],
                unit_price=float(row["unit_price"]),
                criticality=row["criticality"],
            )

            statement = statement.on_conflict_do_update(
                index_elements=[Medicine.medicine_id],
                set_={
                    "medicine_name": row["medicine_name"],
                    "category": row["category"],
                    "unit": row["unit"],
                    "unit_price": float(row["unit_price"]),
                    "criticality": row["criticality"],
                },
            )

            connection.execute(statement)

    print(f"Medicines loaded: {len(rows)}")


def load_suppliers():
    rows = read_csv("suppliers.csv")

    with engine.begin() as connection:
        for row in rows:

            statement = insert(Supplier).values(
                supplier_id=row["supplier_id"],
                supplier_name=row["supplier_name"],
                contact_email=row["contact_email"],
                lead_time_days=int(row["lead_time_days"]),
                reliability_score=float(row["reliability_score"]),
                location=row["location"],
            )

            statement = statement.on_conflict_do_update(
                index_elements=[Supplier.supplier_id],
                set_={
                    "supplier_name": row["supplier_name"],
                    "contact_email": row["contact_email"],
                    "lead_time_days": int(row["lead_time_days"]),
                    "reliability_score": float(row["reliability_score"]),
                    "location": row["location"],
                },
            )

            connection.execute(statement)

    print(f"Suppliers loaded: {len(rows)}")


def load_inventory():
    rows = read_csv("inventory.csv")

    with engine.begin() as connection:
        for row in rows:

            statement = insert(Inventory).values(
                medicine_id=row["medicine_id"],
                current_stock=int(row["current_stock"]),
                reorder_level=int(row["reorder_level"]),
                safety_stock=int(row["safety_stock"]),
                expiry_date=to_date(row["expiry_date"]),
                supplier_id=row["supplier_id"],
                last_restock_date=to_date(row["last_restock_date"]),
            )

            statement = statement.on_conflict_do_update(
                index_elements=[Inventory.medicine_id],
                set_={
                    "current_stock": int(row["current_stock"]),
                    "reorder_level": int(row["reorder_level"]),
                    "safety_stock": int(row["safety_stock"]),
                    "expiry_date": to_date(row["expiry_date"]),
                    "supplier_id": row["supplier_id"],
                    "last_restock_date": to_date(row["last_restock_date"]),
                },
            )

            connection.execute(statement)

    print(f"Inventory records loaded: {len(rows)}")


if __name__ == "__main__":
    load_medicines()
    load_suppliers()
    load_inventory()

    print("All CSV data loaded successfully!")