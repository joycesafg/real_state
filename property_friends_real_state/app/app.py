from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from pymongo import MongoClient
from pathlib import Path
from datetime import datetime
import pandas as pd
import joblib
import os
from pydantic import BaseModel

# MongoDB Configuration
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/logs_db")
client = MongoClient(MONGO_URI)
db = client.logs_db
logs_collection = db.api_logs

# Load trained model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "model.pkl")
model = joblib.load(MODEL_PATH)

# API Key Configuration
API_KEY_NAME = "x-api-key"
API_KEY_VALUE = os.getenv("API_KEY_VALUE", "A1bC3dE5FgH7IjK9LmN0OpQrStUvWxY")  # Preferably use environment variables
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

# Function to validate API Key
def validate_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY_VALUE:
        raise HTTPException(status_code=403, detail="Access denied: Invalid API Key")
    return api_key

# Function to log requests in MongoDB
def log_to_mongo(data: dict):
    try:
        logs_collection.insert_one({"timestamp": datetime.utcnow(), **data})
    except Exception as e:
        print(f"[LOG ERROR] Failed to save log in MongoDB: {e}")

# API input model
class PredictionInput(BaseModel):
    type: str
    sector: str
    net_usable_area: float
    net_area: float
    n_rooms: float
    n_bathroom: float
    latitude: float
    longitude: float
    price: float

# Initialize FastAPI
app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to preprocess input data
def preprocess_input(input_data: PredictionInput) -> pd.DataFrame:
    return pd.DataFrame([input_data.model_dump()])

# Prediction endpoint
@app.post("/predict/", dependencies=[Depends(validate_api_key)])
def predict(input_data: PredictionInput):
    try:
        # Preprocessing
        input_df = preprocess_input(input_data)

        # Model inference
        prediction = model.predict(input_df)
        predicted_value = int(prediction[0])

        # Logging and response
        response = {"input": input_data.model_dump(), "prediction": predicted_value}
        log_to_mongo(response)

        return {"prediction": predicted_value}

    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Input data error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")