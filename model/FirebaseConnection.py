import firebase_admin
import streamlit as st
from firebase_admin import credentials, firestore
from google.cloud.firestore_v1.collection import CollectionReference

class FirebaseConnection:
    def __init__(self, cert : dict[str, ]) -> None:
        self.__init_connection(cert)

    def collection(self, name="") -> CollectionReference:
        return self.__db.collection(name)

    def __init_connection(self, cert : dict[str, ]):
        self.__cred = credentials.Certificate(cert)
        self.__app = firebase_admin.initialize_app(self.__cred, name="fp-rag-utc")
        self.__db = firestore.client(app=self.__app)

@st.cache_resource
def load_connection():
    return FirebaseConnection(dict(st.secrets["connections"]["firebase"]))
