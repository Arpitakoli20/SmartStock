import pandas as pd
from xgboost import XGBRegressor

from ml.utils.data_loader import load_consumption_data
from ml.forecasting.features import create_features


FEATURE_COLUMNS = [
    "lag_1",
    "lag_7",
    "rolling_7",
    "rolling_14",
    "day_of_week",
    "month"
]


def prepare_training_data(df):
    """Prepare feature and target data for XGBoost."""

    df = create_features(df)

    # Remove rows where lag/rolling features are not available
    df = df.dropna(
        subset=FEATURE_COLUMNS + ["quantity_consumed"]
    ).copy()

    X = df[FEATURE_COLUMNS]
    y = df["quantity_consumed"]

    return X, y, df


def train_model(X, y):
    """Train XGBoost demand forecasting model."""

    model = XGBRegressor(
        n_estimators=200,
        max_depth=5,
        learning_rate=0.05,
        objective="reg:squarederror",
        random_state=42
    )

    model.fit(X, y)

    return model


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - XGBOOST FORECAST MODEL")
    print("===================================")

    # Load actual consumption data
    df = load_consumption_data()

    print("\nOriginal data shape:", df.shape)

    # Prepare training data
    X, y, training_df = prepare_training_data(df)

    print("Training data shape:", X.shape)

    print("\nFeatures used:")
    print(FEATURE_COLUMNS)

    # Train model
    model = train_model(X, y)

    print("\nXGBoost model trained successfully!")

    # Test prediction on last record
    sample_features = X.tail(1)

    prediction = model.predict(sample_features)[0]

    print("\nSample prediction:")
    print(round(float(prediction), 2), "units")

    print("\nActual consumption:")
    print(
        float(
            y.tail(1).iloc[0]
        ),
        "units"
    )