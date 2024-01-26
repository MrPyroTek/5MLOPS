import pandas as pd


def prepare_data(data: dict) -> pd.DataFrame:
    index = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca", "thal"]
    return pd.DataFrame(data=data, index=index)
