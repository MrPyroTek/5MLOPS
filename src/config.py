from pathlib import Path

# PATHS
ROOT_DIR = Path(__file__).parent
PATH_LOCAL_DATA = ROOT_DIR / "local_data"

# DATA
CSV_DATA_PATH = PATH_LOCAL_DATA / "HeartDiseaseUCI.csv"

# MLFLOW
MLFLOW_TRACKING_URI = "http://mlflow:5000"
MLFLOW_EXPERIMENT_NAME = "heart_disease_status"
REGISTERED_MODEL_NAME = "heart_disease_model"

# MISC
NUMERICAL_VARS = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'ca']
CATEGORICAL_VARS = ['sex', 'cp', 'fbs', 'restecg', 'exang', 'slope', 'thal']
TARGET_NAME = "potential"
