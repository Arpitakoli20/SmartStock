import pandas as pd
import matplotlib.pyplot as plt


SHAP_PATH = "ml/forecasting/shap_importance.csv"


def create_shap_plot():

    # Load SHAP importance
    df = pd.read_csv(
        SHAP_PATH
    )

    # Sort from highest to lowest
    df = df.sort_values(
        "importance",
        ascending=True
    )

    # Create figure
    plt.figure(
        figsize=(10, 6)
    )

    # Create horizontal bar chart
    plt.barh(
        df["feature"],
        df["importance"]
    )

    # Labels
    plt.xlabel(
        "Mean Absolute SHAP Value"
    )

    plt.ylabel(
        "Feature"
    )

    plt.title(
        "SmartStock - Forecast Model Feature Importance"
    )

    # Add values to bars
    for index, value in enumerate(
        df["importance"]
    ):

        plt.text(
            value,
            index,
            f" {value:.2f}",
            va="center"
        )

    # Improve layout
    plt.tight_layout()

    # Save graph
    output_path = (
        "ml/forecasting/shap_feature_importance.png"
    )

    plt.savefig(
        output_path,
        dpi=300,
        bbox_inches="tight"
    )

    print(
        "SHAP visualization saved to:"
    )

    print(
        output_path
    )

    # Display graph
    plt.show()


if __name__ == "__main__":

    print("===================================")
    print("SMARTSTOCK - SHAP VISUALIZATION")
    print("===================================")

    create_shap_plot()