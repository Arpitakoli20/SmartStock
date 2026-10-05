import pandas as pd


DATA_PATH = "data/consumption.csv"


def load_consumption_data():
    """Load and prepare medicine consumption data."""

    df = pd.read_csv(DATA_PATH)

    # Convert date column to datetime
    df["date"] = pd.to_datetime(df["date"])

    # Make sure quantity is numeric
    df["quantity_consumed"] = pd.to_numeric(
        df["quantity_consumed"],
        errors="coerce"
    )

    # Remove rows with missing important values
    df = df.dropna(
        subset=["date", "medicine_id", "quantity_consumed"]
    )

    # Sort data medicine-wise and date-wise
    df = df.sort_values(
        ["medicine_id", "date"]
    ).reset_index(drop=True)

    return df


if __name__ == "__main__":

    df = load_consumption_data()

    print("===================================")
    print("SMARTSTOCK - CONSUMPTION DATA")
    print("===================================")

    print("\nShape:", df.shape)

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nNumber of medicines:")
    print(df["medicine_id"].nunique())

    print("\nMedicine IDs:")
    print(df["medicine_id"].unique())

    print("\nDate range:")
    print(df["date"].min(), "to", df["date"].max())

    print("\nMissing values:")
    print(df.isnull().sum())

    print("\nFirst 10 records:")
    print(df.head(10))