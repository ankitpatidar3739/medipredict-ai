import streamlit as st
from utils.styles import load_css
from utils.auth   import show_login_page

st.set_page_config(
    page_title="MediPredict AI",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(load_css(), unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username"  not in st.session_state:
    st.session_state.username  = ""
if "name"      not in st.session_state:
    st.session_state.name      = ""

if not st.session_state.logged_in:
    show_login_page()
    st.stop()

# ── Sidebar ────────────────────────────────────────────
with st.sidebar:
    initials = "".join([w[0].upper() for w in st.session_state.name.split()[:2]])
    st.markdown(f"""
    <div class='profile-card'>
        <div class='profile-avatar'>{initials if initials else '👤'}</div>
        <div class='profile-name'>{st.session_state.name}</div>
        <div class='profile-handle'>@{st.session_state.username}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sidebar-section-label'>Navigation</div>",
                unsafe_allow_html=True)
    st.page_link("app.py",               label="Dashboard")
    st.page_link("pages/diabetes.py",  label="Diabetes Predictor")
    st.page_link("pages/heart.py",     label="Heart Disease")
    st.page_link("pages/kidney.py",    label="Kidney Disease")
    st.page_link("pages/analytics.py", label="Analytics")

    st.markdown("---")
    if st.button("Sign Out"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.session_state.name      = ""
        st.rerun()

# ── Hero ───────────────────────────────────────────────
st.markdown("<div class='glow-text'>MediPredict AI</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Clinical Risk Assessment Platform</div>",
            unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ── Disease cards ──────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class='dash-card'>
        <span class='dash-card-icon'>🩸</span>
        <div class='dash-card-title'>Diabetes</div>
        <div class='dash-card-desc'>
            Assess risk using glucose, BMI, insulin levels, and family history indicators.
        </div>
    </div>""", unsafe_allow_html=True)
    if st.button("Open Diabetes Predictor →", key="go_diabetes"):
        st.switch_page("pages/diabetes.py")

with col2:
    st.markdown("""
    <div class='dash-card'>
        <span class='dash-card-icon'>❤️</span>
        <div class='dash-card-title'>Heart Disease</div>
        <div class='dash-card-desc'>
            Evaluate cardiovascular risk via ECG readings, cholesterol, and stress tests.
        </div>
    </div>""", unsafe_allow_html=True)
    if st.button("Open Heart Predictor →", key="go_heart"):
        st.switch_page("pages/heart.py")

with col3:
    st.markdown("""
    <div class='dash-card'>
        <span class='dash-card-icon'>🫘</span>
        <div class='dash-card-title'>Kidney Disease</div>
        <div class='dash-card-desc'>
            Detect CKD risk using creatinine, hemoglobin, and 22 clinical parameters.
        </div>
    </div>""", unsafe_allow_html=True)
    if st.button("Open Kidney Predictor →", key="go_kidney"):
        st.switch_page("pages/kidney.py")

st.markdown("<br>", unsafe_allow_html=True)

# ── Stats row ──────────────────────────────────────────
from utils.auth import get_history
import pandas as pd

history = get_history(st.session_state.username)
total   = len(history)
high    = sum(1 for h in history if "HIGH" in h.get("result",""))
low     = total - high
diseases = len(set(h.get("disease","") for h in history)) if history else 0

s1, s2, s3, s4 = st.columns(4, gap="small")
with s1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Scans</div>
        <div class='metric-value'>{total}</div>
        <div class='metric-sub'>All time predictions</div>
    </div>""", unsafe_allow_html=True)
with s2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>High Risk</div>
        <div class='metric-value' style='color:#F1707A'>{high}</div>
        <div class='metric-sub'>Flagged for review</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Low Risk</div>
        <div class='metric-value' style='color:#4ADE80'>{low}</div>
        <div class='metric-sub'>Within normal range</div>
    </div>""", unsafe_allow_html=True)
with s4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Diseases Screened</div>
        <div class='metric-value'>{diseases}</div>
        <div class='metric-sub'>Unique conditions</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Recent history ─────────────────────────────────────
st.markdown("<div class='section-header'>Recent Predictions</div>",
            unsafe_allow_html=True)

if not history:
    st.info("No predictions yet. Open a disease module to run your first scan.")
else:
    df = pd.DataFrame(history[-10:][::-1])
    df["Result"] = df["result"].apply(
        lambda x: f"{'🔴 ' if 'HIGH' in x else '🟢 '}{x}")
    st.dataframe(
        df[["date","disease","Result","confidence"]].rename(columns={
            "date":"Date", "disease":"Disease",
            "Result":"Result", "confidence":"Confidence"
        }),
        use_container_width=True,
        hide_index=True
    )

st.markdown("""
<div class='footer'>
MediPredict AI &nbsp;·&nbsp; For educational purposes only
&nbsp;·&nbsp; Not a substitute for professional medical advice
</div>""", unsafe_allow_html=True)