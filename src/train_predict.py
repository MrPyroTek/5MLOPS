from typing import Tuple, Any

import pandas as pd
from prefect import flow
from evaluate import evaluate
from train_model import train_model
from predict import predict


@flow(name="Model initialisation")
def train_and_predict(
        x_train: pd.DataFrame,
        y_train: pd.DataFrame,
        x_test: pd.DataFrame,
        y_test: pd.DataFrame
) -> tuple:
    """Train model, predict values and calculate error"""
    model = train_model(x_train, y_train)
    prediction = predict(x_test, model)
    score_f1 = evaluate(y_test, prediction)
    return model, score_f1
