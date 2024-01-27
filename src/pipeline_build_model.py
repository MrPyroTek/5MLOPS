import mlflow
from load import load_csv
from preprocess import process_data, transform_data
from train_predict import train_and_predict
from config import CSV_DATA_PATH, MLFLOW_TRACKING_URI, MLFLOW_EXPERIMENT_NAME, REGISTERED_MODEL_NAME
from prefect import flow

@flow(name="Build model flow")
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

        print("Step 2 - Prepocessing data")
        df_clean = process_data(df)

        print("Step 3 - Split data")
        x_train, x_test, y_train, y_test = transform_data(df_clean)

        print("Step 4 - Train and evaluate model")
        knn_model, score_f1 = train_and_predict(x_train,y_train, x_test, y_test)
        
        mlflow.log_param(knn_model.get_params())
        mlflow.log_metric("f1_score",score_f1)
        mlflow.sklearn.log_model(knn_model,
                                 artifact_path="model",
                                 registered_model_name=REGISTERED_MODEL_NAME)
    
    client = mlflow.MlflowClient()
    client.transition_model_version_stage(name=REGISTERED_MODEL_NAME,
                                          version=1,
                                          stage="Developement")



