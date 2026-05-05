import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.styles import load_css
from utils.auth   import get_history

st.set_page_config(page_title="Analytics · MediPredict", page_icon="📊", layout="wide")
st.markdown(load_css(), unsafe_allow_html=True)

if not st.session_state.get("logged_in"):
    st.warning("Please sign in to view analytics.")
    st.stop()

PLOTLY_LAYOUT = dict(
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(family='DM Sans, sans-serif', color='#7A8BA8', size=12),
    margin=dict(l=20, r=20, t=30, b=20),
    xaxis=dict(gridcolor='rgba(99,179,237,0.06)',
               linecolor='rgba(99,179,237,0.1)'),
    yaxis=dict(gridcolor='rgba(99,179,237,0.06)',
               linecolor='rgba(99,179,237,0.1)'),
)

st.markdown("<div class='glow-text'>Analytics</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-text'>Prediction History & Risk Insights</div>",
            unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

history = get_history(st.session_state.username)

if not history:
    st.info("No prediction history yet. Run a prediction to see your analytics.")
    st.stop()

df = pd.DataFrame(history)

# ── KPI strip ──────────────────────────────────────────
total     = len(df)
high_risk = len(df[df['result'].str.contains('HIGH')])
low_risk  = total - high_risk
diseases  = df['disease'].nunique()

k1, k2, k3, k4 = st.columns(4, gap="small")
with k1:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Total Predictions</div>
        <div class='metric-value'>{total}</div>
    </div>""", unsafe_allow_html=True)
with k2:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>High Risk</div>
        <div class='metric-value' style='color:#F1707A'>{high_risk}</div>
    </div>""", unsafe_allow_html=True)
with k3:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Low Risk</div>
        <div class='metric-value' style='color:#4ADE80'>{low_risk}</div>
    </div>""", unsafe_allow_html=True)
with k4:
    st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-label'>Diseases Screened</div>
        <div class='metric-value'>{diseases}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts row 1 ───────────────────────────────────────
c1, c2 = st.columns(2, gap="medium")

with c1:
    st.markdown("<div class='section-header'>Risk Distribution</div>",
                unsafe_allow_html=True)
    risk_counts = df['result'].value_counts()
    fig = px.pie(
        values=risk_counts.values,
        names=risk_counts.index,
        color_discrete_sequence=['#F1707A', '#4ADE80'],
        hole=0.55
    )
    fig.update_layout(**PLOTLY_LAYOUT)
    fig.update_traces(
        textfont=dict(color='#C8D0E0', size=12),
        marker=dict(line=dict(color='#060910', width=2))
    )
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.markdown("<div class='section-header'>Predictions by Disease</div>",
                unsafe_allow_html=True)
    dc = df['disease'].value_counts().reset_index()
    dc.columns = ['Disease', 'Count']
    fig2 = px.bar(
        dc, x='Disease', y='Count',
        color='Disease',
        color_discrete_sequence=['#63B3ED', '#F1707A', '#4ADE80']
    )
    fig2.update_layout(**PLOTLY_LAYOUT, showlegend=False)
    fig2.update_traces(marker_line_width=0)
    st.plotly_chart(fig2, use_container_width=True)

# ── Timeline ───────────────────────────────────────────
st.markdown("<div class='section-header'>Prediction Timeline</div>",
            unsafe_allow_html=True)

df['date_parsed'] = pd.to_datetime(df['date'], errors='coerce')
df['risk_num']    = df['result'].apply(lambda x: 1 if 'HIGH' in x else 0)

fig3 = go.Figure()
colors = {'Diabetes': '#63B3ED', 'Heart Disease': '#F1707A', 'Kidney Disease': '#4ADE80'}

for disease in df['disease'].unique():
    sub = df[df['disease'] == disease].sort_values('date_parsed')
    fig3.add_trace(go.Scatter(
        x=sub['date_parsed'],
        y=sub['result'],
        mode='markers+lines',
        name=disease,
        marker=dict(size=10, color=colors.get(disease, '#63B3ED'),
                    line=dict(color='#060910', width=2)),
        line=dict(color=colors.get(disease, '#63B3ED'), width=1.5, dash='dot')
    ))

fig3.update_layout(**PLOTLY_LAYOUT,
    legend=dict(
        bgcolor='rgba(12,18,32,0.8)',
        bordercolor='rgba(99,179,237,0.1)',
        borderwidth=1,
        font=dict(color='#7A8BA8')
    )
)
st.plotly_chart(fig3, use_container_width=True)

# ── Full history table ─────────────────────────────────
st.markdown("<div class='section-header'>Full Prediction Log</div>",
            unsafe_allow_html=True)

df_display = df[['date','disease','result','confidence']].copy()
df_display.columns = ['Date','Disease','Result','Confidence']
df_display = df_display.iloc[::-1].reset_index(drop=True)

st.dataframe(df_display, use_container_width=True, hide_index=True)

st.markdown("""
<div class='footer'>
MediPredict AI &nbsp;·&nbsp; Educational use only
&nbsp;·&nbsp; Not a substitute for professional medical advice
</div>""", unsafe_allow_html=True)