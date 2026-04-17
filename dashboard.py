import streamlit as st
import requests
import time

st.set_page_config(page_title="IoT Maintenance", layout="wide")
st.title("⚙️ IoT Predictive Maintenance Dashboard")

BASE_URL = "https://iot-sensor-monitoring-with-predictive.onrender.com"

st.sidebar.header("Safety Configuration")
threshold = st.sidebar.slider("Critical Health Threshold (%)", 5, 50, 20)

if st.sidebar.button("Retrain AI Engine"):
    try:
        res = requests.post(f"{BASE_URL}/retrain").json()
        st.sidebar.success(res["message"])
    except:
        st.sidebar.error("Retrain failed. Is API awake?")

if st.button("Poll Live Sensors"):
    try:
        # Force JSON response with Headers
        headers = {"Accept": "application/json"}
        
        # 1. Get Sensor Data
        sensor_res = requests.get(f"{BASE_URL}/sensor-stream", headers=headers).json()
        
        # 2. Get Prediction
        params = {"temp": sensor_res['temp'], "vib": sensor_res['vibration'], "press": sensor_res['pressure']}
        pred_res = requests.get(f"{BASE_URL}/predict-maintenance", params=params, headers=headers).json()
        
        life = pred_res['remaining_life_percent']

        # 3. Display Metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Temp", f"{sensor_res['temp']}°C")
        c2.metric("Vibration", f"{sensor_res['vibration']} Hz")
        c3.metric("Pressure", f"{sensor_res['pressure']} PSI")
        c4.metric("Machine Health", f"{life}%")

        if life < threshold:
            st.error(f"🚨 CRITICAL: Action Required for {sensor_res['sensor_id']}!")
        else:
            st.success("✅ System Healthy")
        st.progress(max(0, min(100, int(life))) / 100)

    except Exception as e:
        st.error("API is waking up. Please wait 15 seconds and try again.")
