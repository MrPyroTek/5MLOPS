from fastapi import FastAPI
from pydantic import BaseModel

from app_config import MODEL_VERSION, APP_TITLE, APP_DESCRIPTION, APP_VERSION
from lib.modelling import run_inference

app = FastAPI(title=APP_TITLE,
              description=APP_DESCRIPTION,
              version=APP_VERSION)


class InputData(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: float
    oldpeak: float
    slope: int
    ca: float
    thal: float


class PredictionOut(BaseModel):
    has_heart_disease: bool


@app.get("/")
def home():
    return {"health_check": "OK",
            "model_version": MODEL_VERSION}


@app.post("/predict", response_model=PredictionOut, status_code=201)
def predict(payload: InputData):
    has_heart_disease_int = run_inference(payload.dict())
    return {"has_heart_disease": bool(has_heart_disease_int)}
