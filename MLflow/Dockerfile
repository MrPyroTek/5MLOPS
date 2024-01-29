FROM ghcr.io/mlflow/mlflow:latest

WORKDIR /mlflow/
EXPOSE 5000

ENV BACKEND_URI sqlite:////mlflow/mlflow.db
ENV ARTIFACT_ROOT /mlflow/artifacts
ENV ARTIFACT_DESTINATION /mlflow/artifacts

CMD mlflow server --backend-store-uri ${BACKEND_URI} --host 0.0.0.0 --port 5000
