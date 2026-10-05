import pandas as pd


def create_features(df):
    """Create time-series features for each medicine."""

    df = df.copy()

    df = df.sort_values(
        ["medicine_id", "date"]
    ).reset_index(drop=True)

    # Previous-day consumption
    df["lag_1"] = (
        df.groupby("medicine_id")["quantity_consumed"]
        .shift(1)
    )

    # Consumption 7 days ago
    df["lag_7"] = (
        df.groupby("medicine_id")["quantity_consumed"]
        .shift(7)
    )

    # 7-day rolling average
    df["rolling_7"] = (
        df.groupby("medicine_id")["quantity_consumed"]
        .transform(
            lambda x: x.shift(1).rolling(7).mean()
        )
    )

    # 14-day rolling average
    df["rolling_14"] = (
        df.groupby("medicine_id")["quantity_consumed"]
        .transform(
            lambda x: x.shift(1).rolling(14).mean()
        )
    )

    # Calendar features
    df["day_of_week"] = df["date"].dt.dayofweek
    df["month"] = df["date"].dt.month

    return df


if __name__ == "__main__":

    from ml.utils.data_loader import load_consumption_data

    df = load_consumption_data()

    featured_df = create_features(df)

    print("===================================")
    print("SMARTSTOCK - FORECASTING FEATURES")
    print("===================================")

    print("\nOriginal shape:", df.shape)

    print("Feature shape:", featured_df.shape)

    print("\nNew columns:")

    print(featured_df.columns.tolist())

    print("\nMED001 sample:")

    print(
        featured_df[
            featured_df["medicine_id"] == "MED001"
        ].tail(10)
    )