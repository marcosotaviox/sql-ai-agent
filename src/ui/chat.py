"""
src/ui/chat.py
===============
Chat interface: message history, input, agent reasoning expander.
"""

import streamlit as st
from src.utils.session import append_message
from src.core.agent import run_query


def render_chat() -> None:
    # Display chat history
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

            # Show agent reasoning steps (collapsed by default)
            if msg["role"] == "assistant" and msg.get("steps"):
                with st.expander("🔍 Agent reasoning steps", expanded=False):
                    for i, (action, observation) in enumerate(msg["steps"], 1):
                        st.markdown(f"**Step {i} — Action:** `{action.tool}`")
                        st.code(str(action.tool_input), language="sql")
                        st.markdown("**Observation:**")
                        st.text(str(observation)[:1000])

    # Handle example query injection from sidebar
    pending = st.session_state.pop("pending_query", None)

    # Chat input
    user_input = st.chat_input(
        "Ask a question about Australian labour market data..."
    )

    question = pending or user_input

    if question:
        # Display user message
        with st.chat_message("user"):
            st.markdown(question)
        append_message("user", question)

        # Run agent
        with st.chat_message("assistant"):
            with st.spinner("Analysing ABS data..."):
                result = run_query(st.session_state.agent, question)

            if result["error"]:
                response = f"⚠️ {result['error']}"
                st.error(response)
            else:
                response = result["answer"]
                st.markdown(response)

                if result["steps"]:
                    with st.expander("🔍 Agent reasoning steps", expanded=False):
                        for i, (action, observation) in enumerate(result["steps"], 1):
                            st.markdown(f"**Step {i} — Action:** `{action.tool}`")
                            st.code(str(action.tool_input), language="sql")
                            st.markdown("**Observation:**")
                            st.text(str(observation)[:1000])

        append_message("assistant", response, result["steps"])
        st.rerun()