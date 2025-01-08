import streamlit as st
from model.FirebaseConnection import FirebaseConnection
from google.cloud.firestore_v1.base_query import FieldFilter

conn = FirebaseConnection(dict(st.secrets["connections"]["firebase"]))

for item in conn.collection("subject_index").get():
    print(item.to_dict())
