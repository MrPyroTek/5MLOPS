import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_graphviz
from sklearn.metrics import classification_report

@task(name="Load", tags=['Serialize'])
def load_pickle(path: str):
    with open(path, 'rb') as f:
        loaded_obj = pickle.load(f)
    return loaded_obj


@task(name="Save", tags=['Serialize'])
def save_pickle(path: str, obj: dict):
    with open(path, 'wb') as f:
        pickle.dump(obj, f)

@task(name='load_data', tags=['preprocessing'], retries=2, retry_delay_seconds=60)
def load_data(path: str) -> pd.DataFrame:
    return df = pd.read_csv(path, index_col=0)

@task(name='compute_yhat_binarization', tags=['preprocessing'])
def compute_target(
        df: pd.DataFrame,
) -> pd.DataFrame:
    """
    Cree un Yhat binaire
    """
    df["num"] = np.where(df["num"] >= 1, 1, 0)
    return df

@task(name='encode_cat_cols', tags=['preprocessing'])
def encode_categorical_cols(
        df: pd.DataFrame,
        categorical_cols: List[str] = None
) -> pd.DataFrame:
    if categorical_cols is None:
        categorical_cols = config.CATEGORICAL_VARS
    df[categorical_cols] = df[categorical_cols].fillna(-1).astype('int')
    df[categorical_cols] = df[categorical_cols].astype('str')
    return df

