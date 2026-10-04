from pathlib import Path
import random
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
MEDICINES_FILE = BASE_DIR / "data" / "medicines.csv"
OUTPUT_FILE = BASE_DIR / "data" / "consumption.csv"

# Reproducible data
random.seed(42)

# Read medicines
medicines = pd.read_csv(MEDICINES_FILE)

# Generate 12 months of daily consumption
dates = pd.date_range(
    start="2025-01-01",
    end="2025-12-31",
    freq="D"
)

records = []

for _, medicine in medicines.iterrows():

    medicine_id = medicine["medicine_id"]

    # Base demand for each medicine
    base_demand = random.randint(20, 100)

    for date in dates:

        # Small random variation
        variation = random.randint(-10, 10)

        quantity = max(1, base_demand + variation)

        # Weekend demand slightly lower
        if date.weekday() >= 5:
            quantity = max(1, int(quantity * 0.85))

        # Occasional demand spike
        if random.random() < 0.05:
            quantity = int(quantity * 1.4)

        records.append({
            "date": date.date(),
            "medicine_id": medicine_id,
            "quantity_consumed": quantity,
            "demand_type": "Normal"
        })

# Create DataFrame
df = pd.DataFrame(records)

# Save CSV
df.to_csv(OUTPUT_FILE, index=False)

print("Consumption data generated successfully!")
print(f"Total records: {len(df)}")
print(f"Medicines: {df['medicine_id'].nunique()}")
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Saved to: {OUTPUT_FILE}")