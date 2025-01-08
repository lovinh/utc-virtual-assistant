import streamlit as st
# from model.db_connection import Connection
from model.FirebaseConnection import load_connection
# from firebase_connection import load_connection # Debug only
import pandas as pd
from typing import Literal


class SubjectIndexModel():
    def __init__(self, collection_name: str = "subject_index") -> None:
        super().__init__()
        self.__conn = load_connection()
        self.__collection_ref = self.__conn.collection(collection_name)
        self.ID = "id"
        self.ICON = "icon"
        self.INDEX_NAME = "index_name"
        self.STATUS = "status"
        self.SUBJECT_NAME = "subject_name"
        self.__load_data()

    def __load_data(self) -> None:
        self.__data : pd.DataFrame = pd.DataFrame([{"id" : item.id, **item.to_dict()} for item in list(self.__collection_ref.stream())])
        self.__data.set_index('id', inplace=True)

    @property
    def data(self) -> pd.DataFrame:
        return self.__data

    def update(self, record_id, data : dict):
        try:
            self.__collection_ref.document(record_id).update(data)
            return True
        except Exception as Ex:
            print(Ex)
            return False
        
    def edit_name(self, index: int, new_name: str) -> bool:
        self.__data.iloc[index, self.__data.columns.get_loc(self.SUBJECT_NAME)] = new_name
        id = self.__data.index[index]
        return self.update(id, {self.SUBJECT_NAME : new_name})
        
    
    def change_status(self, index : int | str) -> bool:
        new_status = ""
        if isinstance(index, str):
            index = self.__data.index.get_loc(index)
        if self.__data.iloc[index, self.__data.columns.get_loc(self.STATUS)] == "available":
            self.__data.iloc[index, self.__data.columns.get_loc(self.STATUS)] = "unavailable"
            new_status = "unavailable"
        else:
            self.__data.iloc[index, self.__data.columns.get_loc(self.STATUS)] = "available"
            new_status = "available"
        return self.update(self.__data.index[index], {self.STATUS : new_status})
    
    def delete(self, index) -> bool:
        try:
            self.__data.drop(index, inplace=True)
            self.__collection_ref.document(self.__data.index[index]).delete()
            return True
        except Exception as Ex:
            print(Ex)
            return False
    
    def create_name(self, name) -> bool:
        try:
            if name in self.__data[self.SUBJECT_NAME].values:
                return False
            new_name = {
                self.ICON : "",
                self.INDEX_NAME : "",
                self.STATUS : "unavailable",
                self.SUBJECT_NAME : name
            }
            self.__collection_ref.add(new_name)
            self.__load_data()
            return True
        except Exception as Ex:
            print(Ex)
            return False

    def get_list_subject_name(self) -> list[str]:
        return self.__data[self.SUBJECT_NAME].tolist()
    
    def set_index(self, subject_name, index_name) -> bool:
        self.__data.loc[self.__data[self.SUBJECT_NAME] == subject_name, self.INDEX_NAME] = index_name
        id = self.__data.index[self.__data[self.SUBJECT_NAME] == subject_name][0]
        return self.update(id, {self.INDEX_NAME : index_name})
    
    def get_subject_index_name(self, index_name) -> str | None:
        for i, row in self.__data.iterrows():
            if (row[self.INDEX_NAME] == index_name):
                return row[self.SUBJECT_NAME]
        return None

    def set_icon(self, index : int, icon_string : str) -> bool:
        self.__data.iloc[index, self.__data.columns.get_loc(self.ICON)] = icon_string
        return self.update(self.__data.index[index], {self.ICON : icon_string})
    
    def get_subject_index(self, status : Literal["available", "unavailable"] = None):
        if status == None or status not in ("available", "unavailable"):
            return self.__data.to_dict(orient="records")
        return self.__data[self.__data[self.STATUS] == status].to_dict(orient="records")
    
    def get_index(self, subject_name : str) -> str:
        for i, row in self.__data.iterrows():
            if (row[self.SUBJECT_NAME] == subject_name):
                return row[self.INDEX_NAME]
        return None
    
    def get_info(self, subject_name : str) -> str:
        res = self.__data[self.__data[self.SUBJECT_NAME] == subject_name].to_dict(orient="records")
        if len(res) == 0:
            return None
        return res[0]
    
if __name__ == "__main__":
    subject_index_model = SubjectIndexModel()
    print("before\n", subject_index_model.data)
    # print(subject_index_model.set_index("test-name", "hihi"))
    # print("after\n", subject_index_model.data)