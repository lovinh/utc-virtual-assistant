import streamlit as st
from helpers.string_handler import *
from helpers.cipher import *
from model.model import Model
from model.FirebaseConnection import load_connection, FirebaseConnection
import datetime
from langchain_core.messages import HumanMessage
import os


def render_chat_bot(subject_index : dict[str, str]) -> None:
    conn = load_connection()
    pinecone_api_ref = conn.collection("api").document("pinecone")
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    PINECONE_API_KEY = decrypt_aes(pinecone_api_ref.get().to_dict().get("value"))
    MODEL = st.secrets["MODEL"]
    EMBEDDING = st.secrets["EMBEDDING"]
    INDEX = subject_index.get("index_name")
    STATUS = subject_index.get("status")
    if STATUS == "unavailable" or INDEX is None or INDEX == "":
        with st.container():
            st.markdown(
                '<h1 style="text-align: center">😕 503 </h1>', unsafe_allow_html=True)
            st.markdown(
                '<h1 style="text-align: center">Tư vấn viên chưa sẵn sàng</h1>', unsafe_allow_html=True)
    else:
        try:
            ###### Data section ######
            model = Model(
                model_name=MODEL,
                embedding_name=EMBEDDING,
                index_name=INDEX,
                openai_api_key=OPENAI_API_KEY,
                pinecone_api_key=PINECONE_API_KEY,
                prompt_file=os.path.join(os.getcwd(), "data", "prompt-template.txt")
            )

            ##### Page section #####

            if "chat_history" not in st.session_state:
                st.session_state.chat_history = []

            st.title("🤖 UTC Virtual Assistant - v0.1")

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
                # User query
                st.session_state.chat_history.append(HumanMessage(user_query))
                with st.chat_message(
                    name="user",
                ):
                    st.markdown(user_query)

                # AI response
                ai_response = None
                with st.spinner("Đang phản hồi..."):
                    ai_response = model.get_rag(st.session_state.chat_history)
                ai_response_msg = ai_response[0]
                st.session_state.chat_history.append(ai_response_msg)
                with st.chat_message(name="AI"):
                    st.markdown(ai_response_msg.content)

                # Update question to db
                current_time = datetime.datetime.now()
                conn.collection("questions").add(
                    {
                        "content": user_query,
                        "cost": ai_response[1],
                        "datetime": current_time,
                        "label": "unpredicted"
                    }
                )
        except Exception as Ex:
            print("Chatbot::Error::", Ex)
            with st.container():
                st.markdown(
                    '<h1 style="text-align: center">😕 503 </h1>', unsafe_allow_html=True)
                st.markdown(
                    '<h1 style="text-align: center">Tư vấn viên chưa sẵn sàng</h1>', unsafe_allow_html=True)
