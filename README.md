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

### Deploiement
For deploying environement, use this command :
```bash
docker compose up
```
That create, build, pull image and network.

### Test all is working
Go to the URL `http://localhost:5000` to see MLflow dashboard.