"""
app.py
=======
SQL AI Agent — ABS Australian Labour Force Data
Entry point for the Streamlit application.

Run: streamlit run app.py
"""

import streamlit as st
from dotenv import load_dotenv

from src.utils.session import init_session
from src.ui.sidebar import render_sidebar
from src.ui.chat import render_chat

load_dotenv()

st.set_page_config(
    page_title="SQL AI Agent | ABS Labour Data",
    page_icon="🦘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS — dark glassmorphic style
st.markdown("""
<style>
    .stChatMessage { border-radius: 12px; margin-bottom: 8px; }
    .stChatInputContainer { border-top: 1px solid #1E293B; }
    .main-header {
        background: linear-gradient(135deg, #0A0E1A 0%, #111827 100%);
        border: 1px solid #1E293B;
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
    }
    .badge {
        display: inline-block;
        background: rgba(0, 229, 204, 0.1);
        border: 1px solid rgba(0, 229, 204, 0.3);
        color: #00E5CC;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h2 style="margin:0; color:#E2E8F0;">🦘 SQL AI Agent</h2>
    <p style="margin:4px 0 12px; color:#64748B;">
        Natural language queries over ABS Australian Labour Force data
    </p>
    <span class="badge">Claude claude-sonnet-4-5</span>
    <span class="badge">LangChain ReAct</span>
    <span class="badge">SQLite · ABS Data</span>
    <span class="badge">Read-only · Safe</span>
</div>
""", unsafe_allow_html=True)

init_session()
render_sidebar()
render_chat()