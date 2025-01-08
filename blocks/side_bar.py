import streamlit as st
import logging


def render_side_bar() -> None:
    """
    Render side bar for the application.
    """
    with st.sidebar:
        with st.container():
            st.page_link(
                "app.py", label="Tư vấn viên", icon=":material/home:")
                
        st.divider()
        with st.container():
            st.page_link("pages/feedback.py", label="Feedback",
                         icon=":material/feedback:")
