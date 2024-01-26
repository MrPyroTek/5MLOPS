import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.metrics import classification_report
from prefect import task, flow
from typing import List


# @task(name='load_data', tags=['preprocessing'], retries=2, retry_delay_seconds=60)
# def load_data(path: str) -> pd.DataFrame:
#     return pd.read_csv(path, index_col=0)


@task(name='compute_yhat_binarization', tags=['preprocessing'])
def compute_target(
        df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cree un Yhat binaire
    """
    df["num"] = np.where(df["num"] >= 1, 1, 0)
    return df

@task(name='numeric_imputer', tags=['preprocessing'])
def numeric_imputer(df, numerical_features):
    # Create a numeric transformer pipeline
    numeric_transformer = Pipeline(steps=[("imputation", SimpleImputer(strategy="mean"))])

    # Apply the transformer to the specified numerical features
    df[numerical_features] = numeric_transformer.fit_transform(df[numerical_features])

    return df

@task(name='categorical_imputer', tags=['preprocessing'])
def categorical_imputer(df, categorical_features):
    # Create a categorical transformer pipeline
    categorical_transformer = Pipeline(steps=[
        ("imputation", SimpleImputer(strategy="most_frequent"))
    ])

    # Apply the transformer to the specified categorical features
    df[categorical_features] = categorical_transformer.fit_transform(df[categorical_features])

    return df

@task(name='categorical_encoder', tags=['preprocessing'])
def categorical_encoder(df, categorical_features):
    # Create a categorical encoder transformer pipeline
    categorical_transformer = Pipeline(steps=[
        ("imputation", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder())
    ])

    # Apply the transformer to the specified categorical features
    df_encoded = categorical_transformer.fit_transform(df[categorical_features])

    # Concatenate the encoded features to the original dataframe
    df = pd.concat([df, pd.DataFrame(df_encoded.toarray(),
                                     columns=categorical_transformer.named_steps['encoder'].get_feature_names_out(
                                         categorical_features))], axis=1)

    # Drop the original categorical features
    df = df.drop(categorical_features, axis=1)

    return df


@flow(name="Data processing", retries=1, retry_delay_seconds=30)
def process_data(df):
    df = df.drop(["num"], axis=1)
    df = compute_target(df)
    numerical_features = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']
    categorical_features = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
    df = numeric_imputer(df, numerical_features)
    df = categorical_imputer(df, categorical_features)
    df = categorical_encoder(df, categorical_features)
    return df
