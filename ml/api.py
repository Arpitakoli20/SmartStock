from fastapi import FastAPI, HTTPException
import pandas as pd


RESULTS_PATH = "ml/results/smartstock_ml_results.csv"


app = FastAPI(
    title="SmartStock ML API",
    description="Forecasting, Risk Analysis and Reorder Recommendation API",
    version="1.0.0"
)


def load_results():
    """Load final ML results."""

    return pd.read_csv(
        RESULTS_PATH
    )


@app.get("/")
def home():

    return {
        "message": "SmartStock ML API is running"
    }


@app.get("/ml/results")
def get_all_results():

    df = load_results()

    return df.to_dict(
        orient="records"
    )


@app.get("/ml/results/{medicine_id}")
def get_medicine_result(
    medicine_id: str
):

    df = load_results()

    medicine = df[
        df["medicine_id"] == medicine_id
    ]

    if medicine.empty:

        raise HTTPException(
            status_code=404,
            detail="Medicine not found"
        )

    return medicine.iloc[0].to_dict()


@app.get("/ml/high-risk")
def get_high_risk_medicines():

    df = load_results()

    high_risk = df[
        df["risk_level"] == "HIGH"
    ]

    return high_risk.to_dict(
        orient="records"
    )


@app.get("/ml/reorder")
def get_reorder_recommendations():

    df = load_results()

    reorder = df[
        df["reorder_required"] == True
    ]

    return reorder.to_dict(
        orient="records"
    )