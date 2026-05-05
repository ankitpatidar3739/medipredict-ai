import streamlit as st
import pickle, numpy as np
import shap, matplotlib.pyplot as plt
from utils.styles import load_css
from utils.auth   import save_prediction
from utils.report import generate_report
import os

st.set_page_config(page_title="Diabetes · MediPredict", page_icon="🩸", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("Please sign in to access the predictor.")
    st.stop()

@st.cache_resource
def load():
    m = pickle.load(open('models/model_diabetes.pkl',  'rb'))
    s = pickle.load(open('models/scaler_diabetes.pkl', 'rb'))
    return m, s

model, scaler = load()

# ── Header ─────────────────────────────────────────────
st.markdown("<div class='glow-text'>Diabetes Risk Assessment</div>",
            unsafe_allow_html=True)
st.markdown("<div class='sub-text'>PIMA Indians Diabetes Dataset · XGBoost · SHAP</div>",
            unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Input form ─────────────────────────────────────────
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<div class='section-header'>Patient Information</div>",
                unsafe_allow_html=True)
    patient_name   = st.text_input("Patient Name", placeholder="Full name for report")
    pregnancies    = st.slider("Pregnancies",                     0,  17,   3)
    glucose        = st.slider("Glucose Level (mg/dL)",           0, 200, 110)
    blood_pressure = st.slider("Blood Pressure (mmHg)",           0, 122,  70)
    skin_thickness = st.slider("Skin Thickness (mm)",             0,  99,  20)

with col2:
    st.markdown("<div class='section-header'>Lab Values</div>",
                unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    insulin = st.slider("Insulin Level (IU/mL)",          0, 846,  80)
    bmi     = st.slider("BMI",                          10.0, 67.0, 24.0)
    dpf     = st.slider("Diabetes Pedigree Function",   0.0,  2.5,  0.35)
    age     = st.slider("Age",                           21,  81,   30)

st.markdown("<hr>", unsafe_allow_html=True)

if st.button("Run Diabetes Risk Assessment →", key="diabetes_predict"):
    if not patient_name:
        st.warning("Enter patient name to generate a report.")
    else:
        inp    = np.array([[pregnancies, glucose, blood_pressure,
                            skin_thickness, insulin, bmi, dpf, age]])
        scaled = scaler.transform(inp)
        pred   = model.predict(scaled)[0]
        prob   = model.predict_proba(scaled)[0][1]

        # ── Result ─────────────────────────────────────
        if pred == 1:
            st.markdown(f"""
            <div class='risk-high'>
                <h2>⚠ High Diabetes Risk Detected</h2>
                <h3>Confidence: {prob:.1%}</h3>
                <p>Immediate medical consultation recommended.</p>
            </div>""", unsafe_allow_html=True)
            result = "HIGH RISK"
            risk_factors = [
                f"Glucose {glucose} mg/dL — {'critically elevated' if glucose>180 else 'elevated above normal range'}.",
                f"BMI {bmi} — {'obese' if bmi>30 else 'overweight'} category increases risk significantly.",
                f"Insulin {insulin} IU/mL — {'resistance pattern detected' if insulin>200 else 'borderline'}.",
                f"Age {age} — {'high-risk age group' if age>45 else 'risk increases with age'}.",
                f"Pedigree score {dpf:.2f} — {'strong' if dpf>0.8 else 'moderate'} family history indicator."
            ]
        else:
            st.markdown(f"""
            <div class='risk-low'>
                <h2>✓ Low Diabetes Risk</h2>
                <h3>Confidence: {1-prob:.1%}</h3>
                <p>Maintain healthy lifestyle to remain risk-free.</p>
            </div>""", unsafe_allow_html=True)
            result = "LOW RISK"
            risk_factors = [
                "Glucose levels are within the normal range.",
                "BMI is within acceptable limits.",
                "No significant insulin resistance pattern.",
                "Age is not a primary risk factor currently.",
                "Continue regular health check-ups annually."
            ]

        # ── Risk meter ─────────────────────────────────
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

        # ── Key metrics ────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Key Indicators</div>",
                    unsafe_allow_html=True)
        m1, m2, m3, m4 = st.columns(4, gap="small")
        m1.metric("Glucose",  f"{glucose} mg/dL",
                  delta="Elevated" if glucose > 140 else "Normal",
                  delta_color="inverse" if glucose > 140 else "normal")
        m2.metric("BMI", f"{bmi}",
                  delta="High" if bmi > 30 else "Normal",
                  delta_color="inverse" if bmi > 30 else "normal")
        m3.metric("Insulin", f"{insulin} IU/mL",
                  delta="High" if insulin > 200 else "Normal",
                  delta_color="inverse" if insulin > 200 else "normal")
        m4.metric("Age", f"{age} yrs")

        # ── SHAP ───────────────────────────────────────
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Model Explanation (SHAP)</div>",
                    unsafe_allow_html=True)
        try:
            explainer = shap.Explainer(model)
            shap_vals = explainer(scaled)
            fig, ax   = plt.subplots(figsize=(10, 4))
            fig.patch.set_facecolor('#060910')
            ax.set_facecolor('#060910')
            plt.rcParams['text.color']    = '#7A8BA8'
            plt.rcParams['axes.labelcolor'] = '#7A8BA8'
            shap.waterfall_plot(shap_vals[0], max_display=8, show=False)
            st.pyplot(fig)
            plt.close()
        except Exception as e:
            st.info(f"SHAP visualization unavailable: {e}")

        # ── Save & Report ──────────────────────────────
        inputs_dict = {
            "Pregnancies": pregnancies, "Glucose": glucose,
            "Blood Pressure": blood_pressure, "Skin Thickness": skin_thickness,
            "Insulin": insulin, "BMI": bmi, "DPF": dpf, "Age": age
        }
        save_prediction(st.session_state.username,
                        "Diabetes", result, prob, inputs_dict)

        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<div class='section-header'>Patient Report</div>",
                    unsafe_allow_html=True)
        if st.button("Generate PDF Report →", key="diabetes_pdf"):
            fname = generate_report(
                patient_name, st.session_state.username,
                "Diabetes", result, f"{prob:.1%}",
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
&nbsp;·&nbsp; Always consult a licensed physician
</div>""", unsafe_allow_html=True)