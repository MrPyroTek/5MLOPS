import numpy as np

from sklearn.metrics import f1_score
from prefect import task

@task(name="Evaluation", tags=["Model"])
def evaluate(y_real: np.array, y_pred: np.array)-> float:
    """Calculate f1 score from real target value and prediction value"""
    
    return f1_score(y_real,y_pred)