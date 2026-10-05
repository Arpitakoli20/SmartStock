import pandas as pd

from ml.utils.data_loader import load_consumption_data
from ml.forecasting.features import create_features
from ml.forecasting.model import train_model, FEATURE_COLUMNS


FORECAST_DAYS = 7


def train_forecasting_model(df):
    """Train the XGBoost model using historical data."""

    featured_df = create_features(df)

    training_df = featured_df.dropna(
        subset=FEATURE_COLUMNS + ["quantity_consumed"]
    ).copy()

    X = training_df[FEATURE_COLUMNS]
    y = training_df["quantity_consumed"]

    model = train_model(X, y)

    return model


def forecast_medicine(
    model,
    medicine_data,
    days=7
):
    """Forecast demand for one medicine."""

    medicine_data = medicine_data.sort_values(
        "date"
    ).copy()

    # Create features
    featured_data = create_features(
        medicine_data
    )

    # Take the latest available row
    latest_row = featured_data.dropna(
        subset=FEATURE_COLUMNS
    ).tail(1)

    if latest_row.empty:
        return None

    current_features = latest_row[
        FEATURE_COLUMNS
    ]

    daily_prediction = model.predict(
        current_features
    )[0]

    daily_prediction = max(
        0,
        float(daily_prediction)
    )

    total_prediction = (
        daily_prediction * days
    )

    return {
        "daily_forecast": round(
            daily_prediction,
            2
        ),
        "forecast_7_days": round(
            total_prediction,
            2
        )
    }


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - 7 DAY DEMAND FORECAST")
    print("===================================")

    # Load actual data
    df = load_consumption_data()

    print(
        "\nTotal medicines:",
        df["medicine_id"].nunique()
    )

    # Train model
    model = train_forecasting_model(df)

    print(
        "XGBoost model trained successfully."
    )

    print(
        "\nGenerating forecasts..."
    )

    results = []

    # Forecast medicine by medicine
    for medicine_id in sorted(
        df["medicine_id"].unique()
    ):

        medicine_data = df[
            df["medicine_id"] == medicine_id
        ].copy()

        forecast = forecast_medicine(
            model,
            medicine_data,
            FORECAST_DAYS
        )

        if forecast is not None:

            results.append({
                "medicine_id": medicine_id,
                "daily_forecast":
                    forecast["daily_forecast"],
                "forecast_7_days":
                    forecast["forecast_7_days"]
            })

    # Convert results to DataFrame
    forecast_df = pd.DataFrame(results)

    print(
        "\n==================================="
    )
    print(
        "FORECAST RESULTS"
    )
    print(
        "==================================="
    )

    print(
        "\nTotal medicines forecasted:",
        len(forecast_df)
    )

    print(
        "\nFirst 10 medicines:"
    )

    print(
        forecast_df.head(10).to_string(
            index=False
        )
    )

    # Save results
    forecast_df.to_csv(
        "ml/forecasting/forecast_results.csv",
        index=False
    )

    print(
        "\nForecast saved to:"
    )

    print(
        "ml/forecasting/forecast_results.csv"
    )