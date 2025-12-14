from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import os
from typing import List

app = FastAPI()

MODEL_VERSION = os.getenv("MODEL_VERSION", "v1.0.0")
MODEL_PATH = "app/model.pkl"

try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Failed to load model: {e}")

class PredictRequest(BaseModel):
    features: List[float]

class PredictResponse(BaseModel):
    prediction: int
    version: str

class HealthResponse(BaseModel):
    status: str
    version: str
    model_loaded: bool

@app.get("/health", response_model=HealthResponse)
def health():
    return {
        "status": "ok",
        "version": MODEL_VERSION,
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if len(request.features) != 4:
        raise HTTPException(status_code=400, detail="Expected 4 features")
    
    try:
        features = np.array(request.features).reshape(1, -1)
        prediction = int(model.predict(features)[0])
        
        return {
            "prediction": prediction,
            "version": MODEL_VERSION
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")

@app.get("/")
def root():
    return {
        "service": "ML Model API",
        "version": MODEL_VERSION,
        "endpoints": ["/health", "/predict"]
    }
