import pandas as pd
import mlflow
import pickle

from typing import List
from sklearn.pipeline import Pipeline
from app_config import CATEGORICAL_VARS, MODEL_NAME
from mlflow import MlflowClient

def prepare_data(data: dict) -> pd.DataFrame:

    # Preprocessing pipeline
    df = to_dataframe(data)
    df = categorical_encoder(df, CATEGORICAL_VARS)

    return df


def to_dataframe(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    return df


def load_encoder_fit()->Pipeline:
   
    client = MlflowClient()
    #retrieve the id of the run that have set the aliase model to production
    run_id = client.get_model_version_by_alias(MODEL_NAME, "production").run_id
    artifact_path = "onehot_encoder_fit.pkl"

    #dowload artifact
    mlflow_client = mlflow.tracking.MlflowClient()
    mlflow_client.download_artifacts(run_id, artifact_path, "/api/lib")    

    encoder_fit = pickle.load(open("/api/lib/onehot_encoder_fit.pkl","rb"))

    return encoder_fit
    

def categorical_encoder(df: pd.DataFrame,categorical_features: List[str]) -> pd.DataFrame:
    """
    Encode categorical features and return the dataset compute
    """
    categorical_encoder_fit = load_encoder_fit()

    df_encoded = categorical_encoder_fit.transform(df[categorical_features])
    
    df = pd.concat([df, pd.DataFrame(df_encoded.toarray(),
                                     columns=categorical_encoder_fit.named_steps['encoder'].get_feature_names_out(CATEGORICAL_VARS))],
                                     axis=1)
    df = df.drop(CATEGORICAL_VARS, axis=1)

    return df
