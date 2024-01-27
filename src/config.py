# PATHS
PATH_LOCAL_DATA = "local_data"

# DATA
CSV_DATA_PATH = PATH_LOCAL_DATA + "/" + "HeartDiseaseUCI.csv"

# MLFLOW
MLFLOW_TRACKING_URI = "http://mlflow:5000"
MLFLOW_EXPERIMENT_NAME = "heart_disease_status"
REGISTERED_MODEL_NAME = "heart_disease_model"

# VARIABLES NAMES
NUMERICAL_VARS = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']
CATEGORICAL_VARS = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
TARGET_NAME = "potential"
