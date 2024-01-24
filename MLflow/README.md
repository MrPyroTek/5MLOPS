# MLFlow

[MLflow](https://www.mlflow.org/) is an Open Source repository to store and versionalize model, dataset, hyperparameters and metrics.

## Infrastructure 
`Dockerfile` is a file to create an custom image from `ghcr.io/mlflow/mlflow:v2.1.1` and lauch MLflow server.

The `data` folder is bind to the directory `/mflow` on the container and store MLFlow data.

The file `mflows.db` is a SQLite database and contains data about experiement and store experiment artifacts (metrics, hyperparameters, dataset...).

For this moment, `artifacts` is not used.