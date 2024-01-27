import mlflow

from config import CSV_DATA_PATH, MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, REGISTERED_MODEL_NAME
from load import load_csv
from preprocess import process_data, transform_data
from train_predict import train_and_predict

if __name__ == "__main__":
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

    with mlflow.start_run() as run:
        run_id = run.info.run_id
        print(f"run id: {run_id}")
        print(f"artifact_uri: {mlflow.get_artifact_uri()}")
        print(f"registry_uri: {mlflow.get_registry_uri()}")

        df = load_csv(CSV_DATA_PATH)
        df_clean = process_data(df)
        
        x_train, x_test, y_train, y_test = transform_data(df_clean)
        knn_model, f1_score = train_and_predict(x_train, y_train, x_test, y_test)

        mlflow.log_param(knn_model.get_params())
        mlflow.log_metric("f1_score",f1_score)
        mlflow.sklearn.log_model(knn_model,
                                 artifact_path="model",
                                 registered_model_name=REGISTERED_MODEL_NAME)
        

    client = mlflow.MlflowClient()
    client.transition_model_version_stage(name=REGISTERED_MODEL_NAME,
                                          version=1,
                                          stage="Developement")