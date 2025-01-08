import streamlit as st
from model.FirebaseConnection import FirebaseConnection, load_connection
from google.api_core.exceptions import RetryError
import datetime


class Feedback:
    def __init__(self) -> None:
        self.__conn: FirebaseConnection = load_connection()

    def send_feedback(self, feedback: str, subject_id: str | None = None) -> bool:
        current_time = datetime.datetime.now()
        try:
            self.__conn.collection("feedback").add(
                document_data={
                    "created": current_time,
                    "content": feedback
                },
                document_id=subject_id
            )
            print("send feedback success!")
            return True
        except Exception as ex:
            print(f"Failed to send feedback: {ex}")
            return False


@st.cache_resource
def load_feedback_object() -> Feedback:
    return Feedback()
