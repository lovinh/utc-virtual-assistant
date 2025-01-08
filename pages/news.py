from blocks.chat_bot import ChatBot
import streamlit as st

SUBJECT = "Tin tức và hoạt động"

st.set_page_config(
    page_title= SUBJECT + " | UTC Virtual Assistant",
    page_icon="res\icon.png",
)

ChatBot(SUBJECT)