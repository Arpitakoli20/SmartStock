from pathlib import Path
import pandas as pd
from sqlalchemy import insert

from backend.database import engine, Consumption


BASE_DIR = Path(__file__).resolve().parent.parent
CSV_FILE = BASE_DIR / "data" / "consumption.csv"


# Read CSV
df = pd.read_csv(CSV_FILE)

# Convert date column
df["date"] = pd.to_datetime(df["date"]).dt.date

# Convert DataFrame to records
records = df[
    [
        "date",
        "medicine_id",
        "quantity_consumed",
        "demand_type"
    ]
].to_dict(orient="records")


# Insert into database
with engine.begin() as connection:
    connection.execute(insert(Consumption), records)


print("Consumption data loaded successfully!")
print(f"Records inserted: {len(records)}")