import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from prefect import task, flow
from typing import List


@task(name='compute_target', tags=['preprocessing'])
def compute_target(
        df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cree un Yhat binaire correspondant a la potentielle presence ou non d'une maladie cardiaque
    """
    df["potential"] = np.where(df["num"] >= 1, 1, 0)
    df = df.drop(["num"], axis=1)
    return df


@task(name='numeric_imputer', tags=['preprocessing'])
def numeric_imputer(
        df: pd.DataFrame,
        numerical_features: List[str]
) -> pd.DataFrame:
    """
    Impute les valeurs manquantes pour les valeurs numeriques
    """
    numeric_transformer = Pipeline(steps=[("imputation", SimpleImputer(strategy="mean"))])

    df[numerical_features] = numeric_transformer.fit_transform(df[numerical_features])

    return df


@task(name='categorical_imputer', tags=['preprocessing'])
def categorical_imputer(
        df: pd.DataFrame,
        categorical_features: List[str]
) -> pd.DataFrame:
    """
    Impute les valeurs manquantes pour les valeurs categoriques
    """
    categorical_transformer = Pipeline(steps=[
        ("imputation", SimpleImputer(strategy="most_frequent"))
    ])

    df[categorical_features] = categorical_transformer.fit_transform(df[categorical_features])
    return df


@task(name='categorical_encoder', tags=['preprocessing'])
def categorical_encoder(
        df: pd.DataFrame,
        categorical_features: List[str]
) -> pd.DataFrame:
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


@flow(name="process_data", retries=1, retry_delay_seconds=30)
def process_data(
        df: pd.DataFrame
) -> pd.DataFrame:
    """
    process le dataframe
    """
    df = compute_target(df)
    numerical_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']  # Todo: déplacer dans config
    categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
    df = numeric_imputer(df, numerical_features)
    df = categorical_imputer(df, categorical_features)
    df = categorical_encoder(df, categorical_features)
    return df
