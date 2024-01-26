# 5-MLDE
Projet : HeartDiseaseUCI
\
Groupe : Thomas Angama, Théo Frère et Benjamin Fourmaux -- Beruet

[![](https://img.shields.io/badge/Docker-compose?logo=docker&logoColor=white&color=blue)]()
[![](https://img.shields.io/badge/MLflow-using?logo=MLflow&color=white
)]()

## Setup working enviroment
We using [Docker](https://www.docker.com/) as container platform and build containers with Docker compose YAML manifest.

### Containers
list of all used containers :
- `mlflow` : MLflow server
- `api` : Prediction API

### Deploiement
For deploying environement, use this command :
```bash
docker compose up
```
That create, build, pull image and network.

### Test all is working
- Go to the URL `http://localhost:5000` to see MLflow dashboard.
- The prediction API is on the URL `http://localhost:8080`

## Get prediction
To have a prediction of the model, use the HTTP API and send a `POST` request to the `/predict` endpoint, with JSON encoded data in body.

```bash
[POST] http://localhost:8080/predict
```

> You can use [Postman](https://www.postman.com/) tool to send HTTP request. Import the request collection build for this project to have tests request.