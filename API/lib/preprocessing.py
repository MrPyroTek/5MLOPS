import numpy as np
import pandas as pd
from typing import List
from sklearn.pipeline import Pipeline
from app_config import DATA_INDEX, CATEGORICAL_VARS, NUMERICAL_VARS, TARGET_NAME
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder


def prepare_data(data: dict) -> pd.DataFrame:

    # Preprocessing pipeline
    df = to_dataframe(data)
    df = numeric_imputer(df, NUMERICAL_VARS)
    df = categorical_imputer(df, CATEGORICAL_VARS)
    df = categorical_encoder(df, CATEGORICAL_VARS)

    return df


def to_dataframe(data: dict) -> pd.DataFrame:
    return pd.DataFrame(data=data, index=DATA_INDEX)


def numeric_imputer(df: pd.DataFrame, numerical_features: List[str]) -> pd.DataFrame:
    """
    Impute les valeurs manquantes pour les valeurs numeriques
    """
    numeric_transformer = Pipeline(steps=[("imputation", SimpleImputer(strategy="mean"))])

    df[numerical_features] = numeric_transformer.fit_transform(df[numerical_features])

    return df


def categorical_imputer(df: pd.DataFrame, categorical_features: List[str]) -> pd.DataFrame:
    """
    Impute les valeurs manquantes pour les valeurs categoriques
    """
    categorical_transformer = Pipeline(steps=[
        ("imputation", SimpleImputer(strategy="most_frequent"))
    ])

    df[categorical_features] = categorical_transformer.fit_transform(df[categorical_features])

    return df


def categorical_encoder(df: pd.DataFrame, categorical_features: List[str]) -> pd.DataFrame:
    categorical_transformer = Pipeline(steps=[
        ("imputation", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder())
    ])
    """
    Encode les valeurs categoriques
    """
    df_encoded = categorical_transformer.fit_transform(df[categorical_features])

    df = pd.concat([df, pd.DataFrame(df_encoded.toarray(),
                                     columns=categorical_transformer.named_steps['encoder'].get_feature_names_out(
                                         categorical_features))], axis=1)

    # Drop the original categorical features
    df = df.drop(categorical_features, axis=1)

    return df
