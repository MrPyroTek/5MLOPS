import numpy as np
import pandas as pd
import mlflow
import pickle
from typing import List
from sklearn.pipeline import Pipeline
from app_config import DATA_INDEX, CATEGORICAL_VARS, NUMERICAL_VARS, TARGET_NAME, REPO_URL, EXPERIENCE_NAME, MODEL_NAME
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from mlflow import MlflowClient
from mlflow.entities import ViewType

def prepare_data(data: dict) -> pd.DataFrame:

    # Preprocessing pipeline
    df = to_dataframe(data)
    df = categorical_encoder(df, CATEGORICAL_VARS)

    return df


def to_dataframe(data: dict) -> pd.DataFrame:
    return pd.DataFrame(data=data, index=DATA_INDEX)


def load_encoder_fit()->Pipeline:
   
    client = MlflowClient()
    #retrieve the id of the run that have the model aliase set to production
    run_id = client.get_model_version_by_alias(MODEL_NAME, "production").run_id
    artifact_path = "onehot_encoder_fit.pkl"

    #dowload artifact
    mlflow_client = mlflow.tracking.MlflowClient()
    mlflow_client.download_artifacts(run_id, artifact_path, "/api/lib")    

    encoder = pickle.load(open("/api/lib/onehot_encoder_fit.pkl","rb"))

    return encoder
    

def categorical_encoder(df: pd.DataFrame,categorical_features: List[str]) -> pd.DataFrame:
    """
    Encode les valeurs categoriques
    """
    categorical_encoder_fit = load_encoder_fit()
    df_encoded = categorical_encoder_fit.transform(df[categorical_features])

    df = pd.concat([df, pd.DataFrame(df_encoded.toarray(),
                                     columns=categorical_encoder.get_feature_names_out(
                                         categorical_features))], axis=1)

    # Drop the original categorical features
    df = df.drop(categorical_features, axis=1)

    return df
