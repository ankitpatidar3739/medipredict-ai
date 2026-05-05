# 🏥 MediPredict AI

> AI-powered clinical risk assessment platform for Diabetes,
> Heart Disease, and Kidney Disease

**Live Demo → [medipredict.streamlit.app](https://jkdabgnpjaej3dbqzcdk33.streamlit.app)**

---

## Features
- 🩸 **Diabetes Predictor** — PIMA dataset · 91% AUC
- ❤️ **Heart Disease** — Cleveland dataset · 88% AUC  
- 🫘 **Kidney Disease** — UCI CKD dataset · 99% AUC
- 🔎 **SHAP Explainability** — model transparency on every prediction
- 📄 **PDF Reports** — downloadable patient risk reports
- 🔐 **User Auth** — login, signup, prediction history
- 📊 **Analytics Dashboard** — Plotly charts, risk trends

## Tech Stack
| Layer | Tools |
|-------|-------|
| ML Models | XGBoost, Scikit-learn |
| Explainability | SHAP |
| Frontend | Streamlit |
| Charts | Plotly |
| Reports | FPDF2 |
| Deployment | Streamlit Cloud |

## Run Locally
```bash
git clone https://github.com/YOUR_USERNAME/medipredict-ai
cd medipredict-ai
pip install -r requirements.txt
streamlit run app.py
```

## Model Performance
| Disease | Accuracy | AUC-ROC |
|---------|----------|---------|
| Diabetes | ~88% | ~91% |
| Heart Disease | ~87% | ~88% |
| Kidney Disease | ~99% | ~99% |

> ⚠️ For educational purposes only.
> Not a substitute for professional medical advice.
