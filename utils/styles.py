def load_css():
    return """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=Instrument+Serif:ital@0;1&family=JetBrains+Mono:wght@400;500&display=swap');

    /* ── Reset & Base ─────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    .stApp {
        background: #060910;
        color: #C8D0E0;
        font-family: 'DM Sans', sans-serif;
        font-size: 15px;
        line-height: 1.6;
    }

    /* ── Ambient background grid ─────────────────── */
    .stApp::before {
        content: '';
        position: fixed;
        inset: 0;
        background-image:
            linear-gradient(rgba(99,179,237,0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(99,179,237,0.03) 1px, transparent 1px);
        background-size: 40px 40px;
        pointer-events: none;
        z-index: 0;
    }

    /* ── Sidebar ──────────────────────────────────── */
    [data-testid="stSidebar"] {
        background: #080C14 !important;
        border-right: 1px solid rgba(99,179,237,0.08) !important;
    }
    [data-testid="stSidebar"] * { font-family: 'DM Sans', sans-serif !important; }

    /* ── Sidebar nav links ────────────────────────── */
    [data-testid="stSidebarNavLink"] {
        border-radius: 8px !important;
        margin: 2px 0 !important;
        transition: all 0.2s ease !important;
        color: #7A8BA8 !important;
        font-size: 13px !important;
        letter-spacing: 0.01em !important;
    }
    [data-testid="stSidebarNavLink"]:hover {
        background: rgba(99,179,237,0.06) !important;
        color: #C8D0E0 !important;
    }
    [data-testid="stSidebarNavLink"][aria-current="page"] {
        background: rgba(99,179,237,0.1) !important;
        color: #63B3ED !important;
        border-left: 2px solid #63B3ED !important;
    }

    /* ── Main content area ────────────────────────── */
    .main .block-container {
        padding: 2rem 2.5rem !important;
        max-width: 1100px !important;
    }

    /* ── Typography ───────────────────────────────── */
    .glow-text {
        font-family: 'Instrument Serif', serif;
        font-size: 2.8rem;
        font-weight: 400;
        font-style: italic;
        color: #E8EEF8;
        letter-spacing: -0.02em;
        line-height: 1.1;
        text-align: center;
        margin-bottom: 0.4rem;
    }
    .sub-text {
        text-align: center;
        color: #4A5A72;
        font-size: 0.85rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 500;
        margin-bottom: 2.5rem;
    }

    /* ── Dashboard cards ──────────────────────────── */
    .dash-card {
        background: #0C1220;
        border: 1px solid rgba(99,179,237,0.1);
        border-radius: 16px;
        padding: 28px 24px;
        cursor: pointer;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    .dash-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg,
            transparent, rgba(99,179,237,0.3), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .dash-card:hover {
        border-color: rgba(99,179,237,0.25);
        transform: translateY(-2px);
        background: #0E1626;
    }
    .dash-card:hover::before { opacity: 1; }

    .dash-card-icon {
        font-size: 1.8rem;
        margin-bottom: 14px;
        display: block;
    }
    .dash-card-title {
        font-family: 'Instrument Serif', serif;
        font-size: 1.3rem;
        color: #C8D0E0;
        margin-bottom: 8px;
    }
    .dash-card-desc {
        font-size: 0.82rem;
        color: #4A5A72;
        line-height: 1.5;
    }

    /* ── Metric cards ─────────────────────────────── */
    .metric-card {
        background: #0C1220;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 12px;
        padding: 18px 20px;
    }
    .metric-label {
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        color: #3A4A62;
        font-weight: 500;
        margin-bottom: 8px;
    }
    .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        color: #C8D0E0;
        font-weight: 500;
    }
    .metric-sub {
        font-size: 0.75rem;
        color: #3A4A62;
        margin-top: 4px;
    }

    /* ── User profile card ────────────────────────── */
    .profile-card {
        background: #0C1220;
        border: 1px solid rgba(99,179,237,0.08);
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-bottom: 8px;
    }
    .profile-avatar {
        width: 52px;
        height: 52px;
        border-radius: 50%;
        background: linear-gradient(135deg, #1A3A6A, #0F2040);
        border: 1px solid rgba(99,179,237,0.2);
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 12px;
        font-size: 1.4rem;
    }
    .profile-name {
        font-family: 'DM Sans', sans-serif;
        font-weight: 500;
        color: #C8D0E0;
        font-size: 0.95rem;
    }
    .profile-handle {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: #3A4A62;
        margin-top: 3px;
    }

    /* ── Section divider ──────────────────────────── */
    .section-divider {
        border: none;
        border-top: 1px solid rgba(99,179,237,0.07);
        margin: 2rem 0;
    }

    /* ── Risk result boxes ────────────────────────── */
    .risk-high {
        background: #120608;
        border: 1px solid rgba(220,53,69,0.3);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .risk-high::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg,
            transparent, rgba(220,53,69,0.6), transparent);
    }
    .risk-high h2 {
        font-family: 'Instrument Serif', serif;
        font-size: 1.7rem;
        font-weight: 400;
        color: #F1707A;
        margin-bottom: 10px;
    }
    .risk-high h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        color: #C05060;
        margin-bottom: 10px;
    }
    .risk-high p { color: #7A4050; font-size: 0.85rem; }

    .risk-low {
        background: #060F0A;
        border: 1px solid rgba(34,197,94,0.2);
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        position: relative;
        overflow: hidden;
    }
    .risk-low::after {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg,
            transparent, rgba(34,197,94,0.5), transparent);
    }
    .risk-low h2 {
        font-family: 'Instrument Serif', serif;
        font-size: 1.7rem;
        font-weight: 400;
        color: #4ADE80;
        margin-bottom: 10px;
    }
    .risk-low h3 {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.1rem;
        color: #22C55E;
        margin-bottom: 10px;
    }
    .risk-low p { color: #2A5A3A; font-size: 0.85rem; }

    /* ── Section headers ──────────────────────────── */
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #3A4A62;
        font-weight: 500;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid rgba(99,179,237,0.07);
    }

    /* ── Input labels ─────────────────────────────── */
    label[data-testid="stWidgetLabel"] p,
    .stSlider label p,
    .stSelectbox label p,
    .stTextInput label p {
        font-size: 0.78rem !important;
        color: #4A5A72 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 500 !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Sliders ──────────────────────────────────── */
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
        background: #0C1220 !important;
        border: 1px solid rgba(99,179,237,0.3) !important;
        color: #63B3ED !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 11px !important;
        border-radius: 6px !important;
        padding: 2px 6px !important;
    }
    .stSlider [role="slider"] {
        background: #63B3ED !important;
        border: 2px solid #0C1220 !important;
        box-shadow: 0 0 0 3px rgba(99,179,237,0.15) !important;
    }

    /* ── Selectboxes ──────────────────────────────── */
    .stSelectbox [data-baseweb="select"] > div {
        background: #0C1220 !important;
        border: 1px solid rgba(99,179,237,0.12) !important;
        border-radius: 8px !important;
        color: #C8D0E0 !important;
        font-size: 13px !important;
    }
    .stSelectbox [data-baseweb="select"] > div:hover {
        border-color: rgba(99,179,237,0.25) !important;
    }

    /* ── Text inputs ──────────────────────────────── */
    .stTextInput input {
        background: #0C1220 !important;
        border: 1px solid rgba(99,179,237,0.12) !important;
        border-radius: 8px !important;
        color: #C8D0E0 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 14px !important;
        padding: 10px 14px !important;
    }
    .stTextInput input:focus {
        border-color: rgba(99,179,237,0.35) !important;
        box-shadow: 0 0 0 3px rgba(99,179,237,0.08) !important;
    }
    .stTextInput input::placeholder { color: #2A3A52 !important; }

    /* ── Buttons ──────────────────────────────────── */
    .stButton > button {
        background: #0C1220 !important;
        border: 1px solid rgba(99,179,237,0.2) !important;
        border-radius: 10px !important;
        color: #63B3ED !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        letter-spacing: 0.03em !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: rgba(99,179,237,0.08) !important;
        border-color: rgba(99,179,237,0.4) !important;
        color: #90CAF9 !important;
        transform: translateY(-1px) !important;
    }
    .stButton > button:active {
        transform: translateY(0) !important;
    }

    /* ── Primary predict button ───────────────────── */
    .stButton > button[kind="primary"] {
        background: rgba(99,179,237,0.1) !important;
        border: 1px solid rgba(99,179,237,0.35) !important;
        color: #90CAF9 !important;
    }

    /* ── Tabs ─────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: #0C1220 !important;
        border: 1px solid rgba(99,179,237,0.08) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        border-radius: 7px !important;
        color: #4A5A72 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        padding: 8px 18px !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    .stTabs [aria-selected="true"] {
        background: rgba(99,179,237,0.12) !important;
        color: #63B3ED !important;
    }

    /* ── Data table ───────────────────────────────── */
    .stDataFrame {
        border: 1px solid rgba(99,179,237,0.08) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }
    .stDataFrame thead th {
        background: #0C1220 !important;
        color: #4A5A72 !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        font-weight: 500 !important;
        border-bottom: 1px solid rgba(99,179,237,0.08) !important;
    }
    .stDataFrame tbody td {
        background: #080C14 !important;
        color: #C8D0E0 !important;
        font-size: 13px !important;
        border-bottom: 1px solid rgba(255,255,255,0.03) !important;
    }

    /* ── Metrics (st.metric) ──────────────────────── */
    [data-testid="stMetric"] {
        background: #0C1220 !important;
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
    }
    [data-testid="stMetricLabel"] {
        font-size: 0.7rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        color: #3A4A62 !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.4rem !important;
        color: #C8D0E0 !important;
        font-weight: 500 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.75rem !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    /* ── Progress bar ─────────────────────────────── */
    .stProgress > div > div > div {
        background: linear-gradient(90deg, #1A3A6A, #63B3ED) !important;
        border-radius: 4px !important;
    }
    .stProgress > div > div {
        background: #0C1220 !important;
        border-radius: 4px !important;
        border: 1px solid rgba(99,179,237,0.08) !important;
    }

    /* ── Alerts & warnings ────────────────────────── */
    .stAlert {
        background: #0C1220 !important;
        border: 1px solid rgba(99,179,237,0.12) !important;
        border-radius: 10px !important;
        color: #C8D0E0 !important;
    }
    .stInfo {
        border-left: 3px solid #63B3ED !important;
    }
    .stWarning {
        border-left: 3px solid #F6AD55 !important;
    }
    .stSuccess {
        border-left: 3px solid #48BB78 !important;
    }
    .stError {
        border-left: 3px solid #F56565 !important;
    }

    /* ── Download button ──────────────────────────── */
    .stDownloadButton > button {
        background: rgba(72,187,120,0.08) !important;
        border: 1px solid rgba(72,187,120,0.25) !important;
        color: #48BB78 !important;
        border-radius: 10px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 13px !important;
        font-weight: 500 !important;
        width: 100% !important;
        padding: 10px 20px !important;
    }
    .stDownloadButton > button:hover {
        background: rgba(72,187,120,0.14) !important;
        border-color: rgba(72,187,120,0.4) !important;
    }

    /* ── Horizontal rule / divider ────────────────── */
    hr {
        border: none !important;
        border-top: 1px solid rgba(99,179,237,0.07) !important;
        margin: 2rem 0 !important;
    }

    /* ── Headings ─────────────────────────────────── */
    h1, h2, h3, h4 {
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
        color: #C8D0E0 !important;
        letter-spacing: -0.01em !important;
    }
    h3 { font-size: 1rem !important; color: #7A8BA8 !important; }

    /* ── Expander ─────────────────────────────────── */
    .stExpander {
        background: #0C1220 !important;
        border: 1px solid rgba(99,179,237,0.08) !important;
        border-radius: 10px !important;
    }

    /* ── Spinner ──────────────────────────────────── */
    .stSpinner > div {
        border-color: #63B3ED transparent transparent !important;
    }

    /* ── Footer ───────────────────────────────────── */
    .footer {
        text-align: center;
        color: #1E2A3A;
        font-size: 0.75rem;
        padding: 24px 0 8px;
        border-top: 1px solid rgba(99,179,237,0.05);
        margin-top: 48px;
        letter-spacing: 0.03em;
    }

    /* ── Risk score label ─────────────────────────── */
    .risk-range-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.72rem;
        color: #3A4A62;
        margin-top: 4px;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    /* ── Login page card ──────────────────────────── */
    .login-card {
        background: #0C1220;
        border: 1px solid rgba(99,179,237,0.1);
        border-radius: 20px;
        padding: 36px 32px;
        position: relative;
        overflow: hidden;
    }
    .login-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 1px;
        background: linear-gradient(90deg,
            transparent, rgba(99,179,237,0.25), transparent);
    }

    /* ── History table badge ──────────────────────── */
    .badge-high {
        background: rgba(220,53,69,0.12);
        color: #F1707A;
        border: 1px solid rgba(220,53,69,0.2);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.05em;
    }
    .badge-low {
        background: rgba(34,197,94,0.1);
        color: #4ADE80;
        border: 1px solid rgba(34,197,94,0.15);
        border-radius: 6px;
        padding: 2px 8px;
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.05em;
    }

    /* ── Scrollbar ────────────────────────────────── */
    ::-webkit-scrollbar { width: 4px; height: 4px; }
    ::-webkit-scrollbar-track { background: #060910; }
    ::-webkit-scrollbar-thumb {
        background: #1A2A40;
        border-radius: 2px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #253A55; }

    /* ── Plotly charts dark background ───────────── */
    .js-plotly-plot .plotly { background: transparent !important; }

    /* ── Sidebar section label ────────────────────── */
    .sidebar-section-label {
        font-size: 0.65rem;
        text-transform: uppercase;
        letter-spacing: 0.12em;
        color: #2A3A52;
        font-weight: 500;
        padding: 0 8px;
        margin: 12px 0 6px;
    }
    </style>
    """