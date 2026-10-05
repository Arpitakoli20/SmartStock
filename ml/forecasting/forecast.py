from ml.utils.data_loader import load_consumption_data


def prepare_medicine_data(df, medicine_id):
    """Get historical consumption for one medicine."""

    medicine_data = df[
        df["medicine_id"] == medicine_id
    ].copy()

    medicine_data = medicine_data.sort_values("date")

    return medicine_data


def forecast_next_days(medicine_data, days=7):
    """Forecast future demand using recent average consumption."""

    recent_average = (
        medicine_data["quantity_consumed"]
        .tail(7)
        .mean()
    )

    daily_forecast = round(recent_average, 2)

    total_forecast = round(
        daily_forecast * days,
        2
    )

    return daily_forecast, total_forecast


if __name__ == "__main__":

    # Load data
    df = load_consumption_data()

    # Medicine to forecast
    medicine_id = "MED001"

    # Get medicine history
    medicine_data = prepare_medicine_data(
        df,
        medicine_id
    )

    # Forecast next 7 days
    daily_forecast, total_forecast = forecast_next_days(
        medicine_data,
        days=7
    )

    print("===================================")
    print("SMARTSTOCK - DEMAND FORECAST")
    print("===================================")

    print("\nMedicine:", medicine_id)

    print(
        "Historical records:",
        len(medicine_data)
    )

    print(
        "\nAverage daily demand:",
        daily_forecast,
        "units"
    )

    print(
        "\nForecast period:",
        "Next 7 days"
    )

    print(
        "Predicted total demand:",
        total_forecast,
        "units"
    )