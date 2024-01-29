from fastapi import FastAPI
from pydantic import BaseModel

from app_config import MODEL_VERSION, APP_TITLE, APP_DESCRIPTION, APP_VERSION
from lib.modelling import load_model_joblib, load_model, run_inference

app = FastAPI(title=APP_TITLE,
              description=APP_DESCRIPTION,
              version=APP_VERSION)

print("Run API")


class InputData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: float
    thal: float


class PredictionOut(BaseModel):
    has_heart_disease: bool


# Loading model
print("Loading model")
loaded_model = load_model()


@app.get("/")
def home():
    return {"health_check": "OK",
            "model_version": MODEL_VERSION}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(payload: InputData):
    print("Running prediction")
    has_heart_disease_int = run_inference(dict(payload), loaded_model)
    print("response :", has_heart_disease_int)
    return {"has_heart_disease": bool(has_heart_disease_int)}
