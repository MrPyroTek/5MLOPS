import mlflow
import warnings
import pickle

from load import load_csv
from preprocess import process_data, transform_data
from train_predict import train_and_predict
from config import CSV_DATA_PATH, MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, REGISTERED_MODEL_NAME
from prefect import flow

warnings.filterwarnings('ignore')


@flow(name="Process build model Flow")
def pipeline_build_model():

    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)
    
    with mlflow.start_run() as run:
        run_id = run.info.run_id
        print(f"run id: {run_id}")
        print(f"artifact_uri: {mlflow.get_artifact_uri()}")
        print(f"registry_uri: {mlflow.get_registry_uri()}")
    
        print("Step 1 - Load data")
        df = load_csv(CSV_DATA_PATH)

        print("Step 2 - Preprocessing data")
        df_clean, encoder_fit = process_data(df)
        pickle.dump(encoder_fit, open("onehot_encoder_fit.pkl", 'wb'))

        print("Step 3 - Split data")
        x_train, x_test, y_train, y_test = transform_data(df_clean)

        print("Step 4 - Train and evaluate model")
        model, score_f1 = train_and_predict(x_train, y_train, x_test, y_test)
        
        print("Step 5 - Log metrics and model")
        for param_name, param_value in model.get_params().items():
            mlflow.log_param(key=param_name, value=param_value)

        mlflow.log_artifact("onehot_encoder_fit.pkl")
        mlflow.log_metric("f1_score", score_f1)
        mlflow.sklearn.log_model(model,
                                 artifact_path="model",
                                 registered_model_name=REGISTERED_MODEL_NAME,
                                 )
        # Add tag env Staging (newer version of MLflow)
        mlflow.set_tag("env", "production")
    
    client = mlflow.MlflowClient()
    client.transition_model_version_stage(name=REGISTERED_MODEL_NAME,
                                          version=1,
                                          stage="production")


pipeline_build_model()
