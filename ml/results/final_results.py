import pandas as pd


FORECAST_PATH = "ml/forecasting/forecast_results.csv"
RISK_PATH = "ml/risk/risk_results.csv"
REORDER_PATH = "ml/reorder/reorder_results.csv"


def create_final_results():

    # Load all ML outputs
    forecast_df = pd.read_csv(
        FORECAST_PATH
    )

    risk_df = pd.read_csv(
        RISK_PATH
    )

    reorder_df = pd.read_csv(
        REORDER_PATH
    )

    # Keep only required forecast columns
    forecast_df = forecast_df[
        [
            "medicine_id",
            "daily_forecast",
            "forecast_7_days"
        ]
    ]

    # Keep required risk columns
    risk_df = risk_df[
        [
            "medicine_id",
            "current_stock",
            "safety_stock",
            "stock_after_forecast",
            "risk_score",
            "risk_level",
            "supplier_id",
            "expiry_date"
        ]
    ]

    # Keep required reorder columns
    reorder_df = reorder_df[
        [
            "medicine_id",
            "lead_time_days",
            "lead_time_demand",
            "recommended_reorder_quantity",
            "reorder_required",
            "supplier_name",
            "reliability_score"
        ]
    ]

    # Merge forecast + risk
    final_df = pd.merge(
        forecast_df,
        risk_df,
        on="medicine_id",
        how="inner"
    )

    # Merge reorder information
    final_df = pd.merge(
        final_df,
        reorder_df,
        on="medicine_id",
        how="inner"
    )

    # Remove duplicate supplier_id if created
    if "supplier_id_x" in final_df.columns:

        final_df["supplier_id"] = (
            final_df["supplier_id_x"]
        )

        final_df = final_df.drop(
            columns=[
                "supplier_id_x",
                "supplier_id_y"
            ]
        )

    # Sort by risk
    final_df = final_df.sort_values(
        [
            "risk_score",
            "recommended_reorder_quantity"
        ],
        ascending=[
            False,
            False
        ]
    ).reset_index(drop=True)

    return final_df


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - FINAL ML RESULTS")
    print("===================================")

    final_df = create_final_results()

    print(
        "\nTotal medicines:",
        len(final_df)
    )

    print(
        "\nFinal columns:"
    )

    print(
        final_df.columns.tolist()
    )

    print(
        "\n==================================="
    )

    print(
        "TOP 10 MEDICINE RESULTS"
    )

    print(
        "==================================="
    )

    print(
        final_df.head(10).to_string(
            index=False
        )
    )

    # Save final output
    output_path = (
        "ml/results/smartstock_ml_results.csv"
    )

    final_df.to_csv(
        output_path,
        index=False
    )

    print(
        "\nFinal ML results saved to:"
    )

    print(
        output_path
    )