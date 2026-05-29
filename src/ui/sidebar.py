"""
src/ui/sidebar.py
==================
Sidebar: DB schema overview and example queries.
API key is loaded from environment — never exposed in the UI.
"""

import streamlit as st
from src.utils.session import clear_history


EXAMPLE_QUERIES = [
    "Which state had the highest unemployment rate in 2024-Q2?",
    "Compare wage growth across industries in 2023.",
    "What are the top 3 industries by employment in Victoria?",
    "Show the unemployment trend in NSW from 2022 to 2024.",
    "Which industry had the fastest wage growth in 2023-Q4?",
    "Compare interstate migration between QLD and VIC in 2023.",
]


def render_sidebar() -> None:
    with st.sidebar:
        st.markdown("## 📊 Database Schema")
        with st.expander("labour_force", expanded=False):
            st.code(
                "quarter TEXT\nstate TEXT\nindustry TEXT\n"
                "employed_thousands INTEGER\nunemployment_rate REAL\n"
                "participation_rate REAL",
                language="sql",
            )
        with st.expander("wage_growth", expanded=False):
            st.code(
                "quarter TEXT\nindustry TEXT\n"
                "wage_price_index REAL\nannual_growth_pct REAL",
                language="sql",
            )
        with st.expander("state_population", expanded=False):
            st.code(
                "year INTEGER\nstate TEXT\npopulation_thousands INTEGER\n"
                "interstate_migration_net INTEGER\noverseas_migration_net INTEGER",
                language="sql",
            )

        st.divider()

        st.markdown("## 💡 Example Queries")
        for query in EXAMPLE_QUERIES:
            if st.button(query, use_container_width=True, key=f"ex_{query[:20]}"):
                st.session_state["pending_query"] = query

        st.divider()

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            clear_history()
            st.rerun()