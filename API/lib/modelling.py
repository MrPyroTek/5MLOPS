import mlflow
import joblib
from mlflow import MlflowClient
from lib.preprocessing import prepare_data
from app_config import REPO_URL, EXPERIENCE_NAME, MODEL_NAME


def load_model():
    """
    Load model from MLflow repository
    :return: Model
    """
    mlflow.set_tracking_uri(REPO_URL)
    mlflow.set_experiment(EXPERIENCE_NAME)

    model = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}@production")

    return model


def load_model_joblib(model_path: str):
    """
    Load model from a joblib file
    :param model_path: directory to the joblib file
    :return: Model
    """
    return joblib.load(model_path)


def run_inference(data: dict, model: any) -> int:
    """
    Run Preprocessing pipeline on received data and predict with Production model
    :param data: Received data
    :param model: Saved model with Production stage
    :return: A row of prediction
    """

    prepared_data = prepare_data(data)

    pred = model.predict(prepared_data)[0]

    return pred
