import streamlit as st
import requests
import time

st.set_page_config(page_title="IoT Predictive Maintenance", layout="wide")
st.title("⚙️ IoT Sensor & Predictive Maintenance Dashboard")



BASE_URL = "http://127.0.0.1:8000" 

st.sidebar.header("Safety Configuration")
critical_threshold = st.sidebar.slider("Critical Health Threshold (%)", 5, 50, 20)

st.sidebar.markdown("---")
st.sidebar.subheader("Admin Controls")

if st.sidebar.button("Retrain AI Engine"):
    with st.spinner("Analyzing new sensor patterns..."):
        try:

            res = requests.post(f"{BASE_URL}/retrain").json()
            st.sidebar.success(res["message"])
            time.sleep(1)
        except Exception as e:
            st.sidebar.error(f"Retrain failed: {e}")

if st.button("Poll Live Sensors"):
    try:
        sensor_res = requests.get(f"{BASE_URL}/sensor-stream").json()
        
        params = {
            "temp": sensor_res['temp'], 
            "vib": sensor_res['vibration'], 
            "press": sensor_res['pressure']
        }
        pred_res = requests.get(f"{BASE_URL}/predict-maintenance", params=params).json()
        
        life_pct = pred_res['remaining_life_percent']


        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Temperature", f"{sensor_res['temp']}°C")
        col2.metric("Vibration", f"{sensor_res['vibration']} Hz")
        col3.metric("Pressure", f"{sensor_res['pressure']} PSI")
        col4.metric("Machine Health", f"{life_pct}%")


        if life_pct < critical_threshold:
            st.error(f"🚨 CRITICAL: Machine {sensor_res['sensor_id']} requires immediate repair!")
            st.progress(max(0, life_pct/100))
        elif life_pct < 50:
            st.warning("⚠️ Schedule Maintenance: Component wear detected.")
            st.progress(life_pct/100)
        else:
            st.success("✅ System Healthy: Operating within normal parameters.")
            st.progress(life_pct/100)

    except Exception as e:
        st.error(f"Connection Error: Is the API running at {BASE_URL}?\n\nDetails: {e}")

st.divider()
st.caption(f"Backend API Status: {BASE_URL}")
