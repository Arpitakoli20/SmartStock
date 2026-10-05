import pandas as pd
import shap

from ml.utils.data_loader import load_consumption_data
from ml.forecasting.features import create_features
from ml.forecasting.model import train_model, FEATURE_COLUMNS


def prepare_model_data(df):
    """Prepare data for SHAP analysis."""

    featured_df = create_features(df)

    training_df = featured_df.dropna(
        subset=FEATURE_COLUMNS + ["quantity_consumed"]
    ).copy()

    X = training_df[FEATURE_COLUMNS]
    y = training_df["quantity_consumed"]

    return X, y, training_df


def explain_model(model, X):
    """Generate SHAP values for the model."""

    explainer = shap.TreeExplainer(model)

    shap_values = explainer.shap_values(X)

    return explainer, shap_values


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - SHAP EXPLAINABILITY")
    print("===================================")

    # Load data
    df = load_consumption_data()

    # Prepare data
    X, y, training_df = prepare_model_data(df)

    print(
        "\nTraining records:",
        len(X)
    )

    print(
        "Features:",
        FEATURE_COLUMNS
    )

    # Train model
    model = train_model(
        X,
        y
    )

    print(
        "\nXGBoost model trained."
    )

    # Generate SHAP values
    explainer, shap_values = explain_model(
        model,
        X
    )

    print(
        "SHAP values generated successfully."
    )

    # Calculate average feature importance
    importance = pd.DataFrame({
        "feature": FEATURE_COLUMNS,
        "importance": abs(shap_values).mean(axis=0)
    })

    importance = importance.sort_values(
        "importance",
        ascending=False
    ).reset_index(drop=True)

    print(
        "\n==================================="
    )

    print(
        "SHAP FEATURE IMPORTANCE"
    )

    print(
        "==================================="
    )

    print(
        importance.to_string(
            index=False
        )
    )

    # Save importance
    output_path = (
        "ml/forecasting/shap_importance.csv"
    )

    importance.to_csv(
        output_path,
        index=False
    )

    print(
        "\nSHAP importance saved to:"
    )

    print(
        output_path
    )