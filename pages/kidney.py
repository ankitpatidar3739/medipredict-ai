import streamlit as st
import pickle, numpy as np
import shap, matplotlib.pyplot as plt
from utils.styles import load_css
from utils.auth   import save_prediction
from utils.report import generate_report
import os

st.set_page_config(page_title="Kidney Disease", page_icon="🫘", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("Please login first!")
    st.stop()

@st.cache_resource
def load():
    m = pickle.load(open('models/model_kidney.pkl', 'rb'))
    s = pickle.load(open('models/scaler_kidney.pkl', 'rb'))
    return m, s

model, scaler = load()

st.markdown("<div class='glow-text'>🫘 Kidney Disease Risk Predictor</div>",
            unsafe_allow_html=True)
st.markdown("<div class='sub-text'>CKD risk assessment using clinical parameters</div>",
            unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📋 Basic Info")
    patient_name = st.text_input("Patient Name", placeholder="Enter patient name")
    age_k = st.slider("Age",                       2,   90,  35)
    bp    = st.slider("Blood Pressure (mm/Hg)",   50,  180,  80)
    sg    = st.selectbox("Specific Gravity",
                         [1.005, 1.010, 1.015, 1.020, 1.025],
                         index=3)                       # default 1.020
    al    = st.selectbox("Albumin (0-5)",          [0, 1, 2, 3, 4, 5])
    su    = st.selectbox("Sugar (0-5)",            [0, 1, 2, 3, 4, 5])

    rbc   = st.selectbox("Red Blood Cells",        ["Normal (0)", "Abnormal (1)"])
    rbc_v = int(rbc[-2])

    pc    = st.selectbox("Pus Cell",               ["Normal (0)", "Abnormal (1)"])
    pc_v  = int(pc[-2])

    pcc   = st.selectbox("Pus Cell Clumps",        ["No (0)", "Yes (1)"])
    pcc_v = int(pcc[-2])

    ba    = st.selectbox("Bacteria",               ["No (0)", "Yes (1)"])
    ba_v  = int(ba[-2])

    bgr   = st.slider("Blood Glucose Random",      70,  490, 100)
    bu    = st.slider("Blood Urea",                 1,  400,  25)

with col2:
    st.markdown("#### 🔬 Lab Values")
    sc    = st.slider("Serum Creatinine",          0.4, 76.0,  0.9)
    sod   = st.slider("Sodium (mEq/L)",           111,  163,  139)
    pot   = st.slider("Potassium (mEq/L)",         2.5, 47.0,  4.4)
    hemo  = st.slider("Hemoglobin (g/dL)",         3.1, 17.8, 14.0)
    pcv   = st.slider("Packed Cell Volume (%)",      9,   54,   44)
    wc    = st.slider("WBC Count (cells/cumm)",  2200, 26400, 7500)
    rc    = st.slider("RBC Count (mill/cmm)",      2.1,  8.0,  5.0)

    htn   = st.selectbox("Hypertension",           ["No (0)", "Yes (1)"])
    htn_v = int(htn[-2])

    dm    = st.selectbox("Diabetes Mellitus",      ["No (0)", "Yes (1)"])
    dm_v  = int(dm[-2])

    cad   = st.selectbox("Coronary Artery Disease",["No (0)", "Yes (1)"])
    cad_v = int(cad[-2])

    appet   = st.selectbox("Appetite",
                           ["Poor (0)", "Good (1)"],
                           index=1)                     # default Good
    appet_v = int(appet[-2])                            # ← FIXED

    pe    = st.selectbox("Pedal Edema",            ["No (0)", "Yes (1)"])
    pe_v  = int(pe[-2])

    ane   = st.selectbox("Anemia",                 ["No (0)", "Yes (1)"])
    ane_v = int(ane[-2])

st.markdown("---")

if st.button("🔍 Predict Kidney Disease Risk"):
    if not patient_name:
        st.warning("Please enter patient name!")
    else:
        inp = np.array([[age_k, bp, sg, al, su,
                         rbc_v, pc_v, pcc_v, ba_v,
                         bgr, bu, sc, sod, pot,
                         hemo, pcv, wc, rc,
                         htn_v, dm_v, cad_v, appet_v, pe_v, ane_v]])

        scaled = scaler.transform(inp)
        pred   = model.predict(scaled)[0]
        prob   = model.predict_proba(scaled)[0][1]

        st.markdown("### 🎯 Prediction Result")

        if pred == 1:
            st.markdown(f"""
            <div class='risk-high'>
                <h2>⚠️ HIGH RISK of Chronic Kidney Disease</h2>
                <h3>Confidence: {prob:.1%}</h3>
                <p>Urgent nephrologist consultation required.</p>
            </div>""", unsafe_allow_html=True)
            result = "HIGH RISK"
            risk_factors = [
                f"Serum Creatinine {sc} — {'severely elevated' if sc > 2 else 'elevated'}.",
                f"Hemoglobin {hemo} g/dL — {'anemia detected' if hemo < 12 else 'borderline'}.",
                f"Blood Urea {bu} — {'high' if bu > 40 else 'borderline'}.",
                "Hypertension is a major CKD driver." if htn_v else "Monitor blood pressure closely.",
                "Diabetes significantly increases CKD risk." if dm_v else "No diabetes flag detected."
            ]
        else:
            st.markdown(f"""
            <div class='risk-low'>
                <h2>✅ LOW RISK of Kidney Disease</h2>
                <h3>Confidence: {1 - prob:.1%}</h3>
                <p>Kidney function appears normal. Continue monitoring.</p>
            </div>""", unsafe_allow_html=True)
            result = "LOW RISK"
            risk_factors = [
                "Creatinine levels are within normal range.",
                "Hemoglobin is adequate — no anemia detected.",
                "Blood urea is normal.",
                "No significant comorbidities detected.",
                "Schedule annual kidney function tests to stay safe."
            ]

        # ── Risk Progress Bar ──────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            st.markdown(f"**📊 Risk Score: {prob:.1%}**")
            st.progress(float(prob))
            st.markdown("""
            <div style='display:flex; justify-content:space-between;
                        font-size:0.8rem; color:#888;'>
                <span>Low Risk</span><span>High Risk</span>
            </div>""", unsafe_allow_html=True)

        # ── SHAP Explanation ───────────────────────────────
        st.markdown("---")
        st.markdown("### 🔎 Why did the model predict this? (SHAP)")
        try:
            explainer = shap.Explainer(model)
            shap_vals = explainer(scaled)
            fig, ax   = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#0f0f1a')
            ax.set_facecolor('#0f0f1a')
            shap.waterfall_plot(shap_vals[0], max_display=12, show=False)
            st.pyplot(fig)
            plt.close()
        except Exception as e:
            st.info(f"SHAP plot skipped: {e}")

        # ── Metric Cards ───────────────────────────────────
        st.markdown("---")
        st.markdown("### 📊 Key Indicators")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Creatinine",  f"{sc} mg/dL",
                  delta="High"   if sc   > 1.2 else "Normal")
        m2.metric("Hemoglobin",  f"{hemo} g/dL",
                  delta="Low"    if hemo < 12   else "Normal")
        m3.metric("Blood Urea",  f"{bu} mg/dL",
                  delta="High"   if bu   > 40   else "Normal")
        m4.metric("Sodium",      f"{sod} mEq/L",
                  delta="Low"    if sod  < 135  else "Normal")

        # ── Save to History ────────────────────────────────
        inputs_dict = {
            "Age":              age_k,
            "Blood Pressure":   bp,
            "Specific Gravity": sg,
            "Serum Creatinine": sc,
            "Hemoglobin":       hemo,
            "Blood Urea":       bu,
            "Sodium":           sod,
            "Hypertension":     htn,
            "Diabetes":         dm,
            "Appetite":         appet
        }
        save_prediction(st.session_state.username,
                        "Kidney Disease", result, prob, inputs_dict)

        # ── PDF Report ─────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📄 Download Medical Report")
        if st.button("📥 Generate PDF Report", key="kidney_pdf"):
            fname = generate_report(
                patient_name,
                st.session_state.username,
                "Kidney Disease",
                result,
                f"{prob:.1%}",
                risk_factors,
                {k: str(v) for k, v in inputs_dict.items()}
            )
            with open(fname, "rb") as f:
                st.download_button(
                    label="⬇️ Download Report PDF",
                    data=f,
                    file_name=fname,
                    mime="application/pdf"
                )
            os.remove(fname)

# ── Footer ─────────────────────────────────────────────
st.markdown("""
<div class='footer'>
⚠️ MediPredict AI is for educational purposes only.
Not a substitute for professional medical advice.
</div>""", unsafe_allow_html=True)