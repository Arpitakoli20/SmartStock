import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error

from ml.utils.data_loader import load_consumption_data
from ml.forecasting.features import create_features
from ml.forecasting.model import train_model, FEATURE_COLUMNS


def prepare_evaluation_data(df):
    """Create features and split data chronologically."""

    df = create_features(df)

    # Remove rows where features are not available
    df = df.dropna(
        subset=FEATURE_COLUMNS + ["quantity_consumed"]
    ).copy()

    # Sort by date
    df = df.sort_values("date").reset_index(drop=True)

    # 80% training, 20% testing
    split_index = int(len(df) * 0.8)

    train_df = df.iloc[:split_index]
    test_df = df.iloc[split_index:]

    X_train = train_df[FEATURE_COLUMNS]
    y_train = train_df["quantity_consumed"]

    X_test = test_df[FEATURE_COLUMNS]
    y_test = test_df["quantity_consumed"]

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - MODEL EVALUATION")
    print("===================================")

    # Load data
    df = load_consumption_data()

    print("\nOriginal data:", df.shape)

    # Prepare train/test data
    X_train, X_test, y_train, y_test = prepare_evaluation_data(df)

    print("Training records:", len(X_train))
    print("Testing records:", len(X_test))

    print(
        "\nTraining period:",
        df["date"].min().date(),
        "to",
        df["date"].iloc[
            int(len(df) * 0.8)
        ].date()
    )

    print(
        "Testing period:",
        df["date"].iloc[
            int(len(df) * 0.8)
        ].date(),
        "to",
        df["date"].max().date()
    )

    # Train model
    model = train_model(X_train, y_train)

    print("\nModel trained successfully.")

    # Predict test data
    predictions = model.predict(X_test)

    # Calculate metrics
    mae = mean_absolute_error(
        y_test,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            y_test,
            predictions
        )
    )

    # MAPE
    non_zero = y_test != 0

    mape = np.mean(
        np.abs(
            (
                y_test[non_zero]
                - predictions[non_zero]
            )
            / y_test[non_zero]
        )
    ) * 100

    print("\n===================================")
    print("MODEL PERFORMANCE")
    print("===================================")

    print("\nMAE:", round(mae, 2), "units")

    print("RMSE:", round(rmse, 2), "units")

    print("MAPE:", round(mape, 2), "%")

    print("\n===================================")
    print("SAMPLE PREDICTIONS")
    print("===================================")

    results = test_df = None

    for i in range(min(10, len(y_test))):

        print(
            "Actual:",
            round(float(y_test.iloc[i]), 2),
            "| Predicted:",
            round(float(predictions[i]), 2)
        )