import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

def trainModel(x_train: pd.DataFrame, y_train: pd.DataFrame)->KNeighborsClassifier:
    """Train and return a KNeighborsClassifier model"""
    hyperparameters_knn = {"n_neighbors" : list(range(2,50)),
                           "p" : [1,2,3,4,5,6],
                           "algorithm" : ["ball_tree", "kd_tree"],
                           "weights" : ["uniform", "distance"]
                           }
    
    grid_search_cv_knn = GridSearchCV(KNeighborsClassifier(),
                                      hyperparameters_knn,
                                      cv = 10,
                                      verbose = 4,
                                      scoring = "f1"
                                      )
    
    best_model_knn = grid_search_cv_knn.fit(x_train, y_train.values.ravel())
    
    return best_model_knn.best_estimator