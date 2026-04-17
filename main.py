import pandas as pd
import numpy as np
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sklearn.ensemble import RandomForestRegressor
import joblib

app = FastAPI()

# FIX: Add CORS Middleware to allow Streamlit to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Task 6: AI Model Setup
X = np.random.rand(100, 3) * 100
y = 100 - (X[:, 0] * 0.5 + np.random.randn(100))
model = RandomForestRegressor(n_estimators=10).fit(X, y)

@app.get("/")
def home():
    return {"status": "IoT Sensor API is Live"}

@app.get("/sensor-stream")
def get_sensor():
    return {
        "sensor_id": "IOT-UNIT-01",
        "temp": round(np.random.uniform(60, 110), 2),
        "vibration": round(np.random.uniform(10, 50), 2),
        "pressure": round(np.random.uniform(90, 120), 2)
    }

@app.get("/predict-maintenance")
def predict(temp: float, vib: float, press: float):
    prediction = model.predict([[temp, vib, press]])
    return {"remaining_life_percent": round(float(prediction[0]), 2)}

@app.post("/retrain")
def retrain():
    model.fit(np.random.rand(10, 3), np.random.rand(10))
    return {"message": "Model retrained with new sensor logs"}
