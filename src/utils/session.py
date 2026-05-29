"""
src/utils/session.py
=====================
Centralised Streamlit session state management.
API key is loaded from environment via python-dotenv.
"""

import os
import streamlit as st
from dotenv import load_dotenv
from src.core.agent import build_agent

load_dotenv()


def init_session() -> None:
    """Initialise all session state keys with defaults."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if "agent" not in st.session_state:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            st.error("ANTHROPIC_API_KEY not found. Check your .env file.")
            st.stop()
        st.session_state.agent = build_agent(api_key)


def append_message(role: str, content: str, steps: list = None) -> None:
    st.session_state.chat_history.append({
        "role": role,
        "content": content,
        "steps": steps or [],
    })


def clear_history() -> None:
    st.session_state.chat_history = []