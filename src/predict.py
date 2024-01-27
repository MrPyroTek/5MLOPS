import numpy as np
import pandas as pd

from sklearn.model_selection import KNeighborsClassifier
from prefect import task

@task(name="Make prediction", tags=["Evaluate"])
def predict(input_data: pd.DataFrame, model_knn: KNeighborsClassifier)->np.array:
    """
    Use trained KNeighborsClassifier model
    to predict target from input data
    :return array of predictions
   """
    
    if len(input_data.shape) == 1:
        data = np.array(input_data).reshape(1,input_data.shape[0])
    elif len(input_data.shape) == 2:
        data = np.array(input_data).reshape(input_data.shape[0],input_data.shape[1])
    
    prediction = model_knn.predict(data)
    
    return np.array(prediction)
