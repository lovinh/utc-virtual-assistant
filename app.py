from blocks.chat_bot import render_chat_bot
from model.SubjectIndexModel import SubjectIndexModel
import streamlit as st


st.set_page_config(
    page_title= "Tư vấn viên" + " | UTC Virtual Assistant",
    page_icon="res\icon.png",
)

subject_index_model = SubjectIndexModel()
active_index = subject_index_model.get_subject_index("available")
active_index_names = [index.get("subject_name") for index in active_index]


# Render the side bar
channel = ""
with st.sidebar:
    with st.container():
            channel = st.selectbox(
            "Lựa chọn tư vấn viên",
            options=active_index_names
        )
    st.divider()
    with st.container():
        st.page_link("pages/feedback.py", label="Feedback",
                        icon=":material/feedback:")

render_chat_bot(subject_index_model.get_info(channel))