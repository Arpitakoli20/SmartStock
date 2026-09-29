from database import engine, Medicine, Supplier, Inventory
from sqlalchemy import select


def check_database():
    with engine.connect() as connection:

        medicines = connection.execute(
            select(Medicine)
        ).fetchall()

        suppliers = connection.execute(
            select(Supplier)
        ).fetchall()

        inventory = connection.execute(
            select(Inventory)
        ).fetchall()

        print("\n===== SMARTSTOCK DATABASE CHECK =====")

        print(f"\nTotal medicines: {len(medicines)}")
        print(f"Total suppliers: {len(suppliers)}")
        print(f"Total inventory records: {len(inventory)}")

        print("\n--- First 5 Medicines ---")
        for medicine in medicines[:5]:
            print(
                medicine.medicine_id,
                "|",
                medicine.medicine_name,
                "|",
                medicine.category,
                "|",
                medicine.criticality
            )

        print("\n--- First 5 Inventory Records ---")
        for item in inventory[:5]:
            print(
                item.medicine_id,
                "| Stock:",
                item.current_stock,
                "| Reorder:",
                item.reorder_level,
                "| Supplier:",
                item.supplier_id
            )

        print("\n===== DATABASE CHECK COMPLETE =====")


if __name__ == "__main__":
    check_database()