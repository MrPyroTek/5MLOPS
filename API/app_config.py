# APP Version
APP_VERSION = "0.0.1"

# MODELS
MODEL_NAME = "heart_disease_model"
MODEL_VERSION = "0.0.1"
EXPERIENCE_NAME = "heart_disease_status"
REPO_URL = "http://mlflow:5000/"
# PATH_TO_MODEL = f"{REPO_URL}models/{MODEL_NAME}/Production"

# API
APP_TITLE = "HeartDiseasePredictionApp"
APP_DESCRIPTION = "A simple API to predict if a patient has a heart disease"

# DATA PREPROCESS
DATA_INDEX = ["age", "sex", "cp", "trestbps", "chol", "fbs", "restecg", "thalach", "exang", "oldpeak", "slope", "ca",
              "thal"]
NUMERICAL_VARS = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']
CATEGORICAL_VARS = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
TARGET_NAME = "potential"
