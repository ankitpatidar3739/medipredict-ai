import streamlit as st
import json
import hashlib
import os
from datetime import datetime

USERS_FILE = "users.json"

def load_users():
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump({}, f)
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password, name):
    users = load_users()
    if username in users:
        return False, "Username already exists."
    users[username] = {
        "name": name,
        "password": hash_password(password),
        "created": datetime.now().strftime("%Y-%m-%d"),
        "history": []
    }
    save_users(users)
    return True, "Account created."

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "Username not found."
    if users[username]["password"] != hash_password(password):
        return False, "Incorrect password."
    return True, users[username]["name"]

def save_prediction(username, disease, result, confidence, inputs):
    users = load_users()
    if username not in users:
        return
    record = {
        "date":       datetime.now().strftime("%Y-%m-%d %H:%M"),
        "disease":    disease,
        "result":     result,
        "confidence": f"{confidence:.1%}",
        "inputs":     inputs
    }
    users[username]["history"].append(record)
    save_users(users)

def get_history(username):
    users = load_users()
    if username not in users:
        return []
    return users[username]["history"]

def show_login_page():
    # ── Hero ───────────────────────────────────────────
    st.markdown("""
    <div style='text-align:center; padding: 3rem 0 1rem;'>
        <div style='
            font-family: "Instrument Serif", serif;
            font-size: 3rem;
            font-weight: 400;
            font-style: italic;
            color: #E8EEF8;
            letter-spacing: -0.02em;
            line-height: 1.1;
            margin-bottom: 0.5rem;
        '>MediPredict AI</div>
        <div style='
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.12em;
            color: #2A3A52;
            font-weight: 500;
        '>Clinical Risk Assessment Platform</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Center column ──────────────────────────────────
    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        st.markdown("<br>", unsafe_allow_html=True)
        tab_login, tab_signup = st.tabs(["Sign In", "Create Account"])

        # ── LOGIN ──────────────────────────────────────
        with tab_login:
            st.markdown("<br>", unsafe_allow_html=True)
            username = st.text_input("Username",
                                     placeholder="your username",
                                     key="login_user")
            password = st.text_input("Password",
                                     type="password",
                                     placeholder="••••••••",
                                     key="login_pass")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Sign In →", key="login_btn"):
                if username and password:
                    success, result = login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username  = username
                        st.session_state.name      = result
                        st.rerun()
                    else:
                        st.error(result)
                else:
                    st.warning("Please fill in all fields.")

            st.markdown("""
            <div style='
                text-align:center;
                color:#2A3A52;
                font-size:0.75rem;
                margin-top:16px;
                font-family: "JetBrains Mono", monospace;
            '>
            demo account &nbsp;·&nbsp; user: demo &nbsp;/&nbsp; pass: demo123
            </div>""", unsafe_allow_html=True)

        # ── SIGNUP ─────────────────────────────────────
        with tab_signup:
            st.markdown("<br>", unsafe_allow_html=True)
            new_name     = st.text_input("Full Name",
                                         placeholder="Dr. Jane Smith",
                                         key="signup_name")
            new_username = st.text_input("Username",
                                         placeholder="choose a username",
                                         key="signup_user")
            new_password = st.text_input("Password",
                                         type="password",
                                         placeholder="min 6 characters",
                                         key="signup_pass")
            confirm_pass = st.text_input("Confirm Password",
                                         type="password",
                                         placeholder="repeat password",
                                         key="confirm_pass")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Create Account →", key="signup_btn"):
                if all([new_name, new_username, new_password, confirm_pass]):
                    if new_password != confirm_pass:
                        st.error("Passwords don't match.")
                    elif len(new_password) < 6:
                        st.error("Password must be at least 6 characters.")
                    else:
                        success, msg = signup(new_username, new_password, new_name)
                        if success:
                            st.success("Account created. Please sign in.")
                        else:
                            st.error(msg)
                else:
                    st.warning("Please fill in all fields.")

    # ── Feature strip ──────────────────────────────────
    st.markdown("<br><br>", unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4, gap="small")
    features = [
        ("🩸", "Diabetes", "PIMA dataset · XGBoost"),
        ("❤️", "Heart Disease", "Cleveland data · XGBoost"),
        ("🫘", "Kidney Disease", "UCI CKD · XGBoost"),
        ("📊", "Analytics", "Full prediction history"),
    ]
    for col, (icon, title, desc) in zip([f1,f2,f3,f4], features):
        with col:
            st.markdown(f"""
            <div style='
                background:#0C1220;
                border:1px solid rgba(99,179,237,0.07);
                border-radius:12px;
                padding:18px 16px;
                text-align:center;
            '>
                <div style='font-size:1.5rem; margin-bottom:8px;'>{icon}</div>
                <div style='
                    font-size:0.85rem;
                    font-weight:500;
                    color:#C8D0E0;
                    margin-bottom:4px;
                '>{title}</div>
                <div style='
                    font-size:0.7rem;
                    color:#2A3A52;
                    font-family:"JetBrains Mono",monospace;
                '>{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div class='footer'>
    MediPredict AI &nbsp;·&nbsp; For educational purposes only
    &nbsp;·&nbsp; Not a substitute for professional medical advice
    </div>""", unsafe_allow_html=True)

    # Create demo account silently
    users = load_users()
    if "demo" not in users:
        signup("demo", "demo123", "Demo User")