# 5-MLDE
Projet : HeartDiseaseUCI
\
Groupe : Thomas Angama, Théo Frère et Benjamin Fourmaux -- Beruet

[![](https://img.shields.io/badge/Docker-compose?logo=docker&logoColor=white&color=blue)]()
[![](https://img.shields.io/badge/MLflow-using?logo=MLflow&color=white
)]()

## Dataset
- `âge` : âge en années
- `sexe` : sexe (1 = masculin, 0 = féminin)
- `cp` : type de douleur thoracique (Valeur 1 : angine typique, Valeur 2 : angine atypique, Valeur 3 : douleur non angineuse, Valeur 4 : asymptomatique)
- `trestbps` : tension artérielle au repos (en mm Hg à l'admission à l'hôpital)
- `chol` : cholestérol sérique en mg/dl
- `fbs` : (glycémie à jeun > 120 mg/dl) (1 = vrai ; 0 = faux)
- `restecg` : résultats électrocardiographiques au repos (Valeur 0 : normal, Valeur 1 : présentant une anomalie de l'onde ST-T (inversions de l'onde T et/ou élévation ou dépression du segment ST > 0,05 mV), Valeur 2 : montrant une hypertrophie ventriculaire gauche probable ou certaine selon Estes Critères)
- `thalach` : fréquence cardiaque maximale atteinte
- `exemple` : angine de poitrine induite par l'effort (1 = oui, 0 = non)
- `oldpeak` = dépression ST induite par l'exercice par rapport au repos
- `pente` : la pente du segment ST d'exercice maximal (Valeur 1 : montante, Valeur 2 : plate, Valeur 3 : descendante)
- `ca` : nombre de gros vaisseaux (0-3) colorés par fluoroscopie
- `thal` : (Valeur 3 : normal, Valeur 6 = défaut fixe, Valeur 7 = défaut réversible)
- `num` : nombre de vaisseaux principaux (0-4) avec un rétrécissement de diamètre > 50 %

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
docker exec -it compute python /app/pipeline_build_model.py
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

### Turn a model into production
The API require a model with alias `production` to get him and predict with.


By default model build from the training pipeline are tagged with `staging`. You need to manually add this `production` alias via the MLflow Dashboard (http://localhost:5000).


Select the desired model and clic on the "Add alias" button on model informations section. Type `production` in the text field and save. Follow the [documentation](https://mlflow.org/docs/latest/model-registry.html#deploy-and-organize-models) if needed.

> Tag are the oldest method to identified production or development model. MLflow preconise to use [alias](https://mlflow.org/docs/latest/model-registry.html#deploy-and-organize-models-with-aliases-and-tags) instead of tag.

## Predictions using API
The API get the model with tag `Production` from MLflow repository and serve it on an endpoint.

To have a prediction of the model, use the HTTP API and send a `POST` request to the `/predict` endpoint, with JSON encoded data in body.

```bash
[POST] http://localhost:8080/predict
```

> You can use [Postman](https://www.postman.com/) tool to send HTTP request. Import `Predict_HeartDiseaseAPI.postman_collection.json`, the request collection build for this project to have tests request.
