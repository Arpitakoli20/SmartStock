import pandas as pd


RISK_PATH = "ml/risk/risk_results.csv"
SUPPLIER_PATH = "data/suppliers.csv"


def calculate_reorder_quantity(row):
    """
    Calculate reorder quantity using supplier lead time.

    Formula:

    Lead-Time Demand =
        Daily Forecast × Supplier Lead Time

    Required Stock =
        Lead-Time Demand + Safety Stock

    Reorder Quantity =
        Required Stock - Current Stock
    """

    current_stock = row["current_stock"]
    daily_forecast = row["daily_forecast"]
    safety_stock = row["safety_stock"]
    lead_time_days = row["lead_time_days"]

    # Expected demand while waiting for supplier
    lead_time_demand = (
        daily_forecast * lead_time_days
    )

    # Required stock to cover lead time
    required_stock = (
        lead_time_demand + safety_stock
    )

    # Amount that needs to be ordered
    reorder_quantity = (
        required_stock - current_stock
    )

    # Never recommend negative quantity
    return max(
        0,
        round(reorder_quantity)
    )


def generate_reorder_recommendations():
    """
    Generate lead-time-aware reorder recommendations.
    """

    # Load risk analysis results
    risk_df = pd.read_csv(
        RISK_PATH
    )

    # Load supplier information
    supplier_df = pd.read_csv(
        SUPPLIER_PATH
    )

    # Merge risk results with supplier data
    df = pd.merge(
        risk_df,
        supplier_df[
            [
                "supplier_id",
                "supplier_name",
                "lead_time_days",
                "reliability_score"
            ]
        ],
        on="supplier_id",
        how="left"
    )

    # ------------------------------------------------
    # Calculate daily forecast
    # ------------------------------------------------
    #
    # risk_results.csv contains forecast_7_days,
    # so we calculate the daily forecast from it.
    #
    df["daily_forecast"] = (
        df["forecast_7_days"] / 7
    )

    # ------------------------------------------------
    # Calculate demand during supplier lead time
    # ------------------------------------------------

    df["lead_time_demand"] = (
        df["daily_forecast"]
        * df["lead_time_days"]
    )

    # ------------------------------------------------
    # Calculate recommended reorder quantity
    # ------------------------------------------------

    df["recommended_reorder_quantity"] = (
        df.apply(
            calculate_reorder_quantity,
            axis=1
        )
    )

    # ------------------------------------------------
    # Determine whether reorder is required
    # ------------------------------------------------

    df["reorder_required"] = (
        df["recommended_reorder_quantity"] > 0
    )

    # ------------------------------------------------
    # Sort results
    # ------------------------------------------------

    df = df.sort_values(
        [
            "risk_score",
            "recommended_reorder_quantity"
        ],
        ascending=[
            False,
            False
        ]
    ).reset_index(drop=True)

    return df


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - LEAD-TIME REORDER")
    print("===================================")

    # Generate recommendations
    reorder_df = (
        generate_reorder_recommendations()
    )

    # ------------------------------------------------
    # Basic information
    # ------------------------------------------------

    print(
        "\nTotal medicines:",
        len(reorder_df)
    )

    reorder_count = (
        reorder_df[
            "reorder_required"
        ].sum()
    )

    print(
        "Medicines requiring reorder:",
        reorder_count
    )

    # ------------------------------------------------
    # Display top recommendations
    # ------------------------------------------------

    print(
        "\n==================================="
    )

    print(
        "TOP REORDER RECOMMENDATIONS"
    )

    print(
        "==================================="
    )

    display_columns = [
        "medicine_id",
        "current_stock",
        "daily_forecast",
        "forecast_7_days",
        "lead_time_days",
        "lead_time_demand",
        "safety_stock",
        "risk_level",
        "recommended_reorder_quantity",
        "supplier_id",
        "supplier_name",
        "reliability_score"
    ]

    print(
        reorder_df[
            display_columns
        ].head(15).to_string(
            index=False
        )
    )

    # ------------------------------------------------
    # Save final recommendations
    # ------------------------------------------------

    output_path = (
        "ml/reorder/reorder_results.csv"
    )

    reorder_df.to_csv(
        output_path,
        index=False
    )

    print(
        "\nLead-time-aware recommendations saved to:"
    )

    print(
        output_path
    )