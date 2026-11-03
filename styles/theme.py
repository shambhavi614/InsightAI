
import streamlit as st


def apply_theme():
    st.markdown(
        """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #0B1516;
    --surface: #142B2C;
    --border: #26534D;
    --primary: #14B8A6;
    --accent: #5EEAD4;
    --text: #E6F7F2;
    --muted: #9AB9B2;
}

.stApp {
    background:
        radial-gradient(
            ellipse at 85% 5%,
            rgba(20,184,166,.12),
            transparent 40%
        ),
        radial-gradient(
            ellipse at 5% 90%,
            rgba(16,185,129,.07),
            transparent 45%
        ),
        var(--bg);
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.block-container {
    max-width: 1450px;
    padding-top: 1.8rem;
    padding-bottom: 3rem;
}

h1, h2, h3 {
    color: var(--text);
}

h1 {
    font-weight: 800 !important;
    letter-spacing: -1.4px !important;
}

[data-testid="stSidebar"] {
    background: #0D1D1F;
    border-right: 1px solid var(--border);
}

[data-testid="stMetric"] {
    background: linear-gradient(
        145deg,
        #173234,
        #102426
    );
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 20px;
    transition:
        transform .25s ease,
        border-color .25s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
    border-color: #14B8A6;
}

[data-testid="stMetricValue"] {
    color: #5EEAD4;
    font-weight: 800;
}

.insight-hero {
    padding: 32px;
    margin: 14px 0 24px;
    border-radius: 24px;
    border: 1px solid rgba(20,184,166,.25);
    background: linear-gradient(
        115deg,
        rgba(20,184,166,.17),
        rgba(9,44,45,.6)
    );
    animation: fadeUp .6s ease both;
}

.insight-hero h2 {
    margin: 0;
    color: #E6F7F2;
    font-size: 29px;
    font-weight: 800;
}

.insight-hero p {
    color: #9AB9B2;
    margin: 10px 0 0;
}

.stButton > button[kind="primary"] {
    background: linear-gradient(
        90deg,
        #0D9488,
        #059669
    );
    color: white;
    border: 0;
    border-radius: 12px;
    font-weight: 600;
}

.stButton > button[kind="secondary"] {
    background: #173234;
    border: 1px solid #26534D;
    color: #E6F7F2;
    border-radius: 11px;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    padding: 7px;
    background: rgba(15,36,38,.85);
    border-radius: 12px;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px;
}

.stTabs [aria-selected="true"] {
    background: rgba(20,184,166,.18);
}

div[data-testid="stChatMessage"] {
    background: rgba(20,43,44,.9);
    border: 1px solid #26534D;
    border-radius: 16px;
}

[data-testid="stExpander"] {
    border: 1px solid #26534D;
    border-radius: 12px;
}

@keyframes fadeUp {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: .01ms !important;
        transition-duration: .01ms !important;
    }
}
</style>
""",
        unsafe_allow_html=True,
    )
