from langchain_openai import ChatOpenAI
from langchain_community.callbacks import get_openai_callback
from langchain_core.messages import AIMessage
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pinecone import Pinecone
from langchain.vectorstores import Pinecone as LCPinecone
from helpers.string_handler import *

class Model:
    def __init__(self, model_name : str, embedding_name : str, openai_api_key : str, pinecone_api_key : str, index_name : str, prompt_file : str) -> None:
        self.__llm : ChatOpenAI = ChatOpenAI(model=model_name)
        self.__embeddings = OpenAIEmbeddings(model=embedding_name)
        self.__pc = Pinecone(api_key=pinecone_api_key)
        self.__index = self.__pc.Index(index_name)
        self.__vectorstore = LCPinecone(
            self.__index, self.__embeddings.embed_query, text_key="text"
        )
        self.__prompt = ChatPromptTemplate.from_messages(
             [
                (
                    "system",
                    read_from_file(prompt_file),
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.__chain = self.__prompt | self.__llm


    def invoke(self, user_query : str, chat_history : list) -> AIMessage:
        ai_response = self.__chain.invoke({
            'messages' : chat_history
        })
        return ai_response

    def get_rag(self, chat_history : list):
        user_query = chat_history[len(chat_history) - 1].content
        ai_response = None
        cost : float = 0
        with get_openai_callback() as cb:
            ai_response = self.__chain.invoke({
                'messages' : chat_history,
                'source_knowledge':"\n\n".join([item.page_content for item in self.retrieve(user_query)])
            })
            cost = cb.total_cost
        return ai_response, cost

    def retrieve(self, user_query : str, top_k : int = 5):
        retrieve_doc = self.__vectorstore.similarity_search(user_query, k=top_k)
        return retrieve_doc

    def get_rag_agent(self, chat_history : list):
        ai_response = self.__agent_executer.invoke({'messages' : chat_history})
        return ai_response
