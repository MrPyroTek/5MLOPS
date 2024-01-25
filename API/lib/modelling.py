import mlflow
import joblib
from lib.preprocessing import prepare_data
from app_config import PATH_TO_MODEL


def load_model(model_path: str):
    """
    Load model from MLflow repository
    :param model_path: URL of the model in the repository
    :return: Model
    """
    return mlflow.pyfunc.load_model(model_uri=model_path)


def load_model_joblib(model_path: str):
    """
    Load model from a joblib file
    :param model_path: directory to the joblib file
    :return: Model
    """
    return joblib.load(model_path)


def run_inference(data: dict) -> int:
    # loaded_model = load_model(PATH_TO_MODEL)
    loaded_model = load_model_joblib("../heart_Disease_prediction.joblib")

    prepared_data = prepare_data(data)

    # return loaded_model.predict(prepared_data)[0]
    return 1
