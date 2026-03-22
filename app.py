import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

st.set_page_config(page_title="AgriAI: Smart Farming", layout="wide")

@st.cache_resource
def load_model():
    model_path = 'models/agronomy_model.pkl'
    if os.path.exists(model_path):
        return joblib.load(model_path)
    else:
        st.error("Model not found! Please run 'python train_model.py' first.")
        return None

model = load_model()

def get_real_market_price(crop_name):
    try:
        df = pd.read_csv("live_market_prices.csv")
        match = df[df['commodity'].str.contains(crop_name, case=False, na=False)]
        if not match.empty:
            price = match['modal_price'].iloc[0]
            return f"₹{price}"
        else:
            return "No data today"
    except FileNotFoundError:
        return "Please run fetch_market_data.py first!"

st.title("🌱 AgriAI: Crop & Market Recommender")
st.markdown("Bridge the gap between soil health and market wealth.")
st.divider()

if model is not None:
    with st.sidebar:
        st.header("Farm Parameters")
        district = st.selectbox("Select District", ["Meerut", "Mathura", "Agra", "Aligarh", "Other"])
        st.subheader("Soil Nutrients (kg/ha)")
        N = st.slider("Nitrogen (N)", 0, 140, 85)
        P = st.slider("Phosphorus (P)", 0, 140, 50)
        K = st.slider("Potassium (K)", 0, 140, 45)
        
        st.subheader("Environment")
        temp = st.number_input("Average Temp (°C)", value=22.0)
        humidity = st.number_input("Humidity (%)", value=80.0)
        ph = st.number_input("Soil pH", value=6.5)
        rainfall = st.number_input("Rainfall (mm)", value=200.0)
        
        analyze_button = st.button("Analyze Data", type="primary", use_container_width=True)

    if analyze_button:
        input_data = pd.DataFrame([[N, P, K, temp, humidity, ph, rainfall]], 
                                   columns=['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall'])
        
        probabilities = model.predict_proba(input_data)[0]
        top_indices = np.argsort(probabilities)[::-1][:2] 
        classes = model.classes_
        
        st.subheader(f"Optimal Strategy for {district} Region")
        
        col1, col2 = st.columns(2)
        
        for i, col in enumerate([col1, col2]):
            crop_name = classes[top_indices[i]]
            match_score = probabilities[top_indices[i]] * 100
            real_price = get_real_market_price(crop_name)
            
            with col:
                st.info(f"### Option {i+1}: {crop_name.capitalize()}")
                st.write(f"**Biological Match:** {match_score:.1f}%")
                st.metric(label="Today's Live Market Price (per Qtl)", value=real_price)
    else:
        st.write("👈 Adjust your soil and weather parameters in the sidebar and click **Analyze Data**.")