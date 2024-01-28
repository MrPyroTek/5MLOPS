import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from prefect import task, flow
from typing import List
from config import TARGET_NAME, NUMERICAL_VARS, CATEGORICAL_VARS


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


@task(name='categorical_inputer', tags=['preprocessing'])
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


@task(name='extract_x_y', tags=['preprocessing'])
def extract_x_y(
        df: pd.DataFrame,
        target: str = TARGET_NAME,
        with_target: bool = True
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Take a dataframe, extract target variable
    :return data without target value and the target values if needed.
    """
    y = None
    if with_target:
        y = df[target]
        df = df.drop(target, axis=1)

    x = df
    return x, y


@task(name="Split_dataset", tags=['preprocessing'])
def split_dataset(x: pd.DataFrame,
                  y: pd.DataFrame
                  ) -> dict:
    """
    Split data into train and test dataset:return x_train, x_test, y_train, y_test
    """

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y)
    y_train = pd.DataFrame(y_train)
    y_test = pd.DataFrame(y_test)

    return {'x_train': x_train, 'x_test': x_test, 'y_train': y_train,  'y_test': y_test}


@flow(name="split_data")
def transform_data(df_clean: pd.DataFrame) -> dict:
    """
    Extract target value from dataset and split it into train and test dataset
    """
    x, y = extract_x_y(df_clean)

    return split_dataset(x=x, y=y).values()


@flow(name="process_data", retries=1, retry_delay_seconds=30)
def process_data(
        df: pd.DataFrame
) -> pd.DataFrame:
    """
    process le dataframe
    """
    df = compute_target(df)
    df = numeric_imputer(df, NUMERICAL_VARS)
    df = categorical_imputer(df, CATEGORICAL_VARS)
    df = categorical_encoder(df, CATEGORICAL_VARS)

    return df
