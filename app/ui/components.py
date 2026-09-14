"""UI components"""

import streamlit as st


def show_statistics_widget(stats: dict):
    """Show statistics widget"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Companies", stats.get('companies_found', 0))
    with col2:
        st.metric("People", stats.get('people_found', 0))
    with col3:
        st.metric("Phones", stats.get('phones_found', 0))
    with col4:
        st.metric("Errors", stats.get('errors', 0))


def show_progress(current: int, total: int, label: str = "Progress"):
    """Show progress bar"""
    progress_pct = (current / total) if total > 0 else 0
    st.progress(progress_pct, text=f"{label} {current}/{total}")
