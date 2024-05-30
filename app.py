import streamlit as st
import os
from dotenv import load_dotenv
from helpers.string import *
from model.model import Model
from langchain_core.messages import HumanMessage
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
MODEL= os.getenv("MODEL")
EMBEDDING= os.getenv("EMBEDDING")
INDEX= os.getenv("INDEX")

model = Model(
    model_name=MODEL,
    embedding_name=EMBEDDING,
    index_name=INDEX,
    openai_api_key=OPENAI_API_KEY,
    pinecone_api_key=PINECONE_API_KEY,
)

st.set_page_config(
    page_title="UTC Virtual Assistant",
    page_icon="res\icon.png"
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("UTC Virtual Assistant - v0.1")

user_query = st.chat_input("Bạn muốn hỏi gì?")
user_query = remove_extra_whitespace(user_query)

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message(name="user"):
            st.markdown(message.content)
    else:
        with st.chat_message(name="AI"):
            st.markdown(message.content)

if user_query is not None and user_query != "":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message(
        name="user",
    ):
        st.markdown(user_query)

    ai_response = model.get_rag(user_query, st.session_state.chat_history)
    st.session_state.chat_history.append(ai_response)

    with st.chat_message(name="AI"):
        # ai_response = model.invoke(user_query)
        st.markdown(ai_response.content)