import streamlit as st
import numpy as np
import pandas as pd
import joblib

# Load model
model = joblib.load("model.pkl")

# Streamlit config
st.set_page_config(page_title="Heart Disease Predictor", page_icon="❤️")

st.title("❤️ Heart Disease Predictor")
st.markdown("Provide medical data to predict heart disease risk.")

# Input form
with st.form("heart_form"):

    age = st.slider("Age", 20, 100, 50)
    trestbps = st.slider("Resting Blood Pressure (mm Hg)", 80, 200, 120)
    chol = st.slider("Serum Cholesterol (mg/dl)", 100, 600, 200)
    fbs = st.radio("Fasting Blood Sugar > 120 mg/dl", ["Yes", "No"], horizontal=True)
    thalch = st.slider("Max Heart Rate Achieved", 60, 220, 150)
    exang = st.radio("Exercise Induced Angina?", ["Yes", "No"], horizontal=True)
    oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0, step=0.1)
    ca = st.selectbox("Number of Major Vessels Colored (0–3)", [0, 1, 2, 3])

    sex = st.radio("Sex", ["Male", "Female"], horizontal=True)
    cp = st.selectbox("Chest Pain Type", ["typical angina", "atypical angina", "non-anginal", "asymptomatic"])
    restecg = st.selectbox("Resting ECG", ["normal", "lv hypertrophy", "st-t abnormality"])
    slope = st.selectbox("Slope of ST Segment", ["upsloping", "flat", "downsloping"])
    thal = st.selectbox("Thalassemia", ["normal", "fixed defect", "reversable defect"])

    submitted = st.form_submit_button("🔍 Predict")

if submitted:
    # Build raw input
    input_dict = {
        'age': age,
        'trestbps': trestbps,
        'chol': chol,
        'fbs': 1 if fbs == "Yes" else 0,
        'thalch': thalch,
        'exang': 1 if exang == "Yes" else 0,
        'oldpeak': oldpeak,
        'ca': ca,
        'sex_Male': 1 if sex == "Male" else 0,
        'cp_atypical angina': int(cp == "atypical angina"),
        'cp_non-anginal': int(cp == "non-anginal"),
        'cp_typical angina': int(cp == "typical angina"),
        'restecg_normal': int(restecg == "normal"),
        'restecg_st-t abnormality': int(restecg == "st-t abnormality"),
        'slope_flat': int(slope == "flat"),
        'slope_upsloping': int(slope == "upsloping"),
        'thal_normal': int(thal == "normal"),
        'thal_reversable defect': int(thal == "reversable defect")
    }

    # Convert to DataFrame
    input_df = pd.DataFrame([input_dict])

    # Ensure column order
    expected_columns = [
        'age', 'trestbps', 'chol', 'fbs', 'thalch', 'exang', 'oldpeak', 'ca',
        'sex_Male', 'cp_atypical angina', 'cp_non-anginal', 'cp_typical angina',
        'restecg_normal', 'restecg_st-t abnormality', 'slope_flat',
        'slope_upsloping', 'thal_normal', 'thal_reversable defect'
    ]

    # Add any missing columns just in case
    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_columns]  # Reorder columns

    # Predict
    prediction = model.predict(input_df)[0]

    st.markdown("## 🩺 Prediction Result")
    if prediction == 1:
        st.error("⚠️ The model predicts **Heart Disease**.")
    else:
        st.success("✅ The model predicts **No Heart Disease**.")

