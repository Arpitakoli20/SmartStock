from pathlib import Path

from sqlalchemy import create_engine, Column, String, Float, Integer, Date, ForeignKey
from sqlalchemy.orm import declarative_base


BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "smartstock.db"

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    echo=False
)

Base = declarative_base()

class Medicine(Base):
    __tablename__ = "medicines"

    medicine_id = Column(String, primary_key=True)
    medicine_name = Column(String, nullable=False)
    category = Column(String)
    unit = Column(String)
    unit_price = Column(Float)
    criticality = Column(String)


class Supplier(Base):
    __tablename__ = "suppliers"

    supplier_id = Column(String, primary_key=True)
    supplier_name = Column(String, nullable=False)
    contact_email = Column(String)
    lead_time_days = Column(Integer)
    reliability_score = Column(Float)
    location = Column(String)


class Inventory(Base):
    __tablename__ = "inventory"

    medicine_id = Column(String, ForeignKey("medicines.medicine_id"), primary_key=True)
    current_stock = Column(Integer, nullable=False)
    reorder_level = Column(Integer)
    safety_stock = Column(Integer)
    expiry_date = Column(Date)
    supplier_id = Column(String, ForeignKey("suppliers.supplier_id"))
    last_restock_date = Column(Date)


class Consumption(Base):
    __tablename__ = "consumption"

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    medicine_id = Column(String, ForeignKey("medicines.medicine_id"), nullable=False)
    quantity_consumed = Column(Integer, nullable=False)
    demand_type = Column(String)


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Database created with 4 tables: medicines, suppliers, inventory, consumption")