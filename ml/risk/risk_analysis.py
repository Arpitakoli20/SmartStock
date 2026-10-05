import pandas as pd


FORECAST_PATH = "ml/forecasting/forecast_results.csv"
INVENTORY_PATH = "data/inventory.csv"


def calculate_risk(row):
    """
    Calculate medicine shortage risk.

    Risk logic:
    HIGH:
        Current stock is less than forecasted demand.

    MEDIUM:
        Current stock can cover demand but falls
        below demand + safety stock.

    LOW:
        Current stock is sufficient including safety stock.
    """

    current_stock = row["current_stock"]
    forecast_7_days = row["forecast_7_days"]
    safety_stock = row["safety_stock"]

    if current_stock < forecast_7_days:
        return "HIGH"

    elif current_stock < (
        forecast_7_days + safety_stock
    ):
        return "MEDIUM"

    else:
        return "LOW"


def calculate_risk_score(row):
    """
    Calculate a simple shortage risk percentage.
    """

    current_stock = row["current_stock"]
    forecast_7_days = row["forecast_7_days"]

    if forecast_7_days <= 0:
        return 0

    stock_coverage = (
        current_stock / forecast_7_days
    )

    if stock_coverage < 0.5:
        return 100

    elif stock_coverage < 0.75:
        return 80

    elif stock_coverage < 1:
        return 60

    elif stock_coverage < 1.25:
        return 40

    else:
        return 20


def perform_risk_analysis():

    # Load forecast results
    forecast_df = pd.read_csv(
        FORECAST_PATH
    )

    # Load inventory data
    inventory_df = pd.read_csv(
        INVENTORY_PATH
    )

    # Merge using medicine_id
    df = pd.merge(
        forecast_df,
        inventory_df,
        on="medicine_id",
        how="inner"
    )

    # Calculate risk level
    df["risk_level"] = df.apply(
        calculate_risk,
        axis=1
    )

    # Calculate risk score
    df["risk_score"] = df.apply(
        calculate_risk_score,
        axis=1
    )

    # Calculate stock after expected demand
    df["stock_after_forecast"] = (
        df["current_stock"]
        - df["forecast_7_days"]
    )

    # Select important columns
    result = df[
        [
            "medicine_id",
            "current_stock",
            "forecast_7_days",
            "safety_stock",
            "stock_after_forecast",
            "risk_score",
            "risk_level",
            "supplier_id",
            "expiry_date"
        ]
    ].copy()

    # Sort highest risk first
    result = result.sort_values(
        ["risk_score", "medicine_id"],
        ascending=[False, True]
    ).reset_index(drop=True)

    return result


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - RISK ANALYSIS")
    print("===================================")

    risk_df = perform_risk_analysis()

    print(
        "\nTotal medicines analyzed:",
        len(risk_df)
    )

    print("\nRisk distribution:")

    print(
        risk_df["risk_level"]
        .value_counts()
    )

    print(
        "\n==================================="
    )
    print("TOP RISK MEDICINES")
    print(
        "==================================="
    )

    print(
        risk_df.head(10).to_string(
            index=False
        )
    )

    # Save results
    output_path = (
        "ml/risk/risk_results.csv"
    )

    risk_df.to_csv(
        output_path,
        index=False
    )

    print(
        "\nRisk analysis saved to:"
    )

    print(output_path)