# 5-MLDE
Projet : HeartDiseaseUCI
\
Groupe : Thomas Angama, Théo Frère et Benjamin Fourmaux -- Beruet

[![](https://img.shields.io/badge/Docker-compose?logo=docker&logoColor=white&color=blue)]()
[![](https://img.shields.io/badge/MLflow-using?logo=MLflow&color=white
)]()

## Dataset
// todo : Add dataset descritption and 

## Setup working enviroment
We using [Docker](https://www.docker.com/) as container platform and build containers with Docker compose YAML manifest.

### Containers
list of all used containers :
- `compute` : Compute container with pipeline and Prefect Dashboard. Image based on [python:3.10.8-slim](https://hub.docker.com/layers/library/python/3.10.8-slim/images/sha256-49749648f4426b31b20fca55ad854caa55ff59dc604f2f76b57d814e0a47c181)
- `mlflow` : MLflow server. Image based on [ghcr.io/mlflow/mlflow](https://github.com/mlflow/mlflow/pkgs/container/mlflow/60538560?tag=v2.1.1)
- `api` : Prediction API. Image based on [python:3.9.0-slim](https://hub.docker.com/layers/library/python/3.9.0-slim/images/sha256-5d300921213569f955c3954787298127d241c115f31fc92e87305c3e7a71c7ef)

### Deploiement
For deploying environement, use this command at the root of the project :
```bash
docker compose up
```
That create, build, pull image and make a network. And run containers

## Prefect Pipeline
To run a pipline inside a container, type the following :
```bash
docker exec -it 5mlde-compute python /app/pipeline_build_model.py
```
and you will see the Prefect pipeline running.

Go to the Prefect dashboard to see the unfolding flow at the URL [`http://localhost:4200`](http://localhost:4200).

## Model repository MLflow
Check model versions and artefacts in the reposritory MLflow via the dashboard at the URL [`http://localhost:5000`](http://localhost:5000).

What is recording ?
- Training datset
- Hyperparameters
- Model
- Metrics (F1, RMSE...)

## Predictions using API
The API get the model with tag `Production` from MLflow repository and serve it on an endpoint.

To have a prediction of the model, use the HTTP API and send a `POST` request to the `/predict` endpoint, with JSON encoded data in body.

```bash
[POST] http://localhost:8080/predict
```

> You can use [Postman](https://www.postman.com/) tool to send HTTP request. Import `Predict_HeartDiseaseAPI.postman_collection.json`, the request collection build for this project to have tests request.