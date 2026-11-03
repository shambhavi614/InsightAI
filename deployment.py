
import os
import streamlit as st


# =========================================================
# INSIGHTAI — DEPLOYMENT CONFIGURATION
# =========================================================

def get_demo_mode():
    """
    Read demo mode from Streamlit Secrets or
    environment variables.

    Supports both Boolean and string values.
    """

    # Default: local AI enabled
    value = os.getenv("INSIGHTAI_DEMO_MODE", "false")

    # Streamlit Cloud secrets override environment
    try:
        value = st.secrets.get(
            "INSIGHTAI_DEMO_MODE",
            value,
        )
    except (FileNotFoundError, OSError):
        pass

    # Convert Boolean or string safely
    return str(value).strip().lower() in (
        "1",
        "true",
        "yes",
        "on",
    )


DEMO_MODE = get_demo_mode()


def ai_available():
    """
    Check whether local Ollama AI is available.
    AI is disabled in public demo mode.
    """

    if DEMO_MODE:
        return False

    try:
        from core.ai_engine import check_ollama

        return bool(check_ollama())

    except Exception:
        return False
