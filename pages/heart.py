import streamlit as st
import pickle, numpy as np
import shap, matplotlib.pyplot as plt
from utils.styles import load_css
from utils.auth   import save_prediction
from utils.report import generate_report
import os

st.set_page_config(page_title="Heart Disease · MediPredict", page_icon="❤️", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("Please sign in to access the predictor.")
    st.stop()

@st.cache_resource
def load():
    m = pickle.load(open('models/model_heart.pkl',  'rb'))
    s = pickle.load(open('models/scaler_heart.pkl', 'rb'))
    return m, s

model, scaler = load()

st.markdown("<div class='glow-text'>Heart Disease Risk Assessment</div>",
            unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Cleveland Heart Disease Dataset · XGBoost · SHAP</div>",
            unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<div class='section-header'>Patient Information</div>",
                unsafe_allow_html=True)
    patient_name = st.text_input("Patient Name", placeholder="Full name for report")
    age_h        = st.slider("Age", 20, 80, 45)
    sex          = st.selectbox("Biological Sex", ["Male (1)", "Female (0)"])
    sex_val      = 1 if "Male" in sex else 0
    cp           = st.selectbox("Chest Pain Type", [
        "0 — Typical Angina",
        "1 — Atypical Angina",
        "2 — Non-anginal Pain",
        "3 — Asymptomatic"
    ])
    cp_val       = int(cp[0])
    trestbps     = st.slider("Resting Blood Pressure (mmHg)", 90, 200, 125)
    chol         = st.slider("Cholesterol (mg/dL)",           100, 600, 220)
    fbs          = st.selectbox("Fasting Blood Sugar > 120 mg/dL",
                                ["No (0)", "Yes (1)"])
    fbs_val      = int(fbs[-2])
    restecg      = st.selectbox("Resting ECG", [
        "0 — Normal",
        "1 — ST-T Wave Abnormality",
        "2 — Left Ventricular Hypertrophy"
    ])
    restecg_val  = int(restecg[0])

with col2:
    st.markdown("<div class='section-header'>Stress Test & ECG</div>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    thalach  = st.slider("Max Heart Rate Achieved",      60, 210, 155)
    exang    = st.selectbox("Exercise Induced Angina",   ["No (0)", "Yes (1)"])
    exang_val= int(exang[-2])
    oldpeak  = st.slider("ST Depression (Oldpeak)",      0.0, 6.2, 0.8)
    slope    = st.selectbox("Slope of ST Segment", [
        "0 — Upsloping",
        "1 — Flat",
        "2 — Downsloping"
    ])
    slope_val = int(slope[0])
    ca        = st.selectbox("Major Vessels Colored (Fluoroscopy)",
                             [0, 1, 2, 3, 4])
    thal      = st.selectbox("Thalassemia", [
        "1 — Normal",
        "2 — Fixed Defect",
        "3 — Reversable Defect"
    ])
    thal_val  = int(thal[0])

st.markdown("<hr>", unsafe_allow_html=True)

if st.button("Run Heart Disease Risk Assessment →", key="heart_predict"):
    if not patient_name:
        st.warning("Enter patient name to generate a report.")
    else:
        inp    = np.array([[age_h, sex_val, cp_val, trestbps, chol,
                            fbs_val, restecg_val, thalach, exang_val,
                            oldpeak, slope_val, ca, thal_val]])
        scaled = scaler.transform(inp)
        pred   = model.predict(scaled)[0]
        prob   = model.predict_proba(scaled)[0][1]

        if pred == 1:
            st.markdown(f"""
            <div class='risk-high'>
                <h2>⚠ High Cardiovascular Risk Detected</h2>
                <h3>Confidence: {prob:.1%}</h3>
                <p>Cardiology referral strongly recommended.</p>
            </div>""", unsafe_allow_html=True)
            result = "HIGH RISK"
            risk_factors = [
                f"Cholesterol {chol} mg/dL — {'dangerously high' if chol>240 else 'borderline high'}.",
                f"Resting BP {trestbps} mmHg — {'hypertensive' if trestbps>140 else 'elevated'}.",
                f"Chest pain type: {cp} — significant cardiac indicator.",
                f"ST depression {oldpeak} — myocardial stress pattern.",
                f"Max HR {thalach} bpm — {'reduced cardiac reserve' if thalach < 120 else 'borderline'}."
            ]
        else:
            st.markdown(f"""
            <div class='risk-low'>
                <h2>✓ Low Cardiovascular Risk</h2>
                <h3>Confidence: {1-prob:.1%}</h3>
                <p>Continue regular cardiac health monitoring.</p>
            </div>""", unsafe_allow_html=True)
            result = "LOW RISK"
            risk_factors = [
                "Cholesterol within acceptable range.",
                "Blood pressure is normal.",
                "No significant ECG abnormalities.",
                "Exercise tolerance appears adequate.",
                "Schedule routine cardiac check-ups annually."
            ]

        st.markdown("<br>", unsafe_allow_html=True)
        _, ctr, _ = st.columns([1, 2, 1])
        with ctr:
            st.markdown(f"""
            <div style='
                font-family:"JetBrains Mono",monospace;
                font-size:0.75rem;
                color:#3A4A62;
                text-transform:uppercase;
                letter-spacing:0.08em;
                margin-bottom:8px;
            '>Risk Score &nbsp; {prob:.1%}</div>""", unsafe_allow_html=True)
            st.progress(float(prob))
            st.markdown("""
            <div class='risk-range-label'>
                <span>Low</span><span>Moderate</span><span>High</span>
            </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Key Indicators</div>",
                    unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4, gap="small")
        m1.metric("Cholesterol", f"{chol} mg/dL",
                  delta="High" if chol > 240 else "Normal",
                  delta_color="inverse" if chol > 240 else "normal")
        m2.metric("Resting BP", f"{trestbps} mmHg",
                  delta="High" if trestbps > 140 else "Normal",
                  delta_color="inverse" if trestbps > 140 else "normal")
        m3.metric("Max HR", f"{thalach} bpm")
        m4.metric("ST Depression", f"{oldpeak}",
                  delta="Elevated" if oldpeak > 2 else "Normal",
                  delta_color="inverse" if oldpeak > 2 else "normal")

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Model Explanation (SHAP)</div>",
                    unsafe_allow_html=True)
        try:
            explainer = shap.Explainer(model)
            shap_vals = explainer(scaled)
            fig, ax   = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#060910')
            ax.set_facecolor('#060910')
            plt.rcParams['text.color']      = '#7A8BA8'
            plt.rcParams['axes.labelcolor'] = '#7A8BA8'
            shap.waterfall_plot(shap_vals[0], max_display=10, show=False)
            st.pyplot(fig)
            plt.close()
        except Exception as e:
            st.info(f"SHAP visualization unavailable: {e}")

        inputs_dict = {
            "Age": age_h, "Sex": sex, "Chest Pain": cp,
            "Resting BP": trestbps, "Cholesterol": chol,
            "Fasting BS": fbs, "Max HR": thalach,
            "Oldpeak": oldpeak, "CA": ca, "Thal": thal
        }
        save_prediction(st.session_state.username,
                        "Heart Disease", result, prob, inputs_dict)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Patient Report</div>",
                    unsafe_allow_html=True)
        if st.button("Generate PDF Report →", key="heart_pdf"):
            fname = generate_report(
                patient_name, st.session_state.username,
                "Heart Disease", result, f"{prob:.1%}",
                risk_factors, {k: str(v) for k, v in inputs_dict.items()}
            )
            with open(fname, "rb") as f:
                st.download_button("Download Report (PDF)",
                                   f, file_name=fname,
                                   mime="application/pdf")
            os.remove(fname)

st.markdown("""
<div class='footer'>
MediPredict AI &nbsp;·&nbsp; Educational use only
&nbsp;·&nbsp; Always consult a licensed cardiologist
</div>""", unsafe_allow_html=True)