import pandas as pd
import numpy as np
from fastapi import FastAPI
from sklearn.ensemble import RandomForestRegressor
import joblib


app = FastAPI()


X = np.random.rand(100, 3) * 100
y = 100 - (X[:, 0] * 0.5 + X[:, 1] * 0.3 + np.random.randn(100)) # RUL simulation
model = RandomForestRegressor().fit(X, y)

@app.get("/")
def home():
    return {"status": "IoT Sensor API is Live"}

@app.get("/sensor-stream")
def get_sensor_data():

    return {
        "sensor_id": "ST-99",
        "temp": round(np.random.uniform(60, 110), 2),
        "vibration": round(np.random.uniform(10, 50), 2),
        "pressure": round(np.random.uniform(90, 120), 2)
    }

@app.get("/predict-maintenance")
def predict(temp: float, vib: float, press: float):

    rul_prediction = model.predict([[temp, vib, press]])
    return {"remaining_life_percent": round(float(rul_prediction), 2)}

@app.post("/retrain")
def retrain():
    return {"message": "Model updated with new machinery wear patterns"}
