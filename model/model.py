from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from pinecone import Pinecone
from langchain.vectorstores import Pinecone as LCPinecone
# from langchain.chains.combine_documents import create_stuff_documents_chain

class Model:
    def __init__(self, model_name : str, embedding_name : str, openai_api_key : str, pinecone_api_key : str, index_name : str) -> None:
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
                    """
Bạn là một nhân viên hỗ trợ sinh viên của trường Đại học Giao thông vận tải với nhiệm vụ trả lời các thắc mắc đến từ sinh viên của trường. Trước hết, bạn phải luôn luôn chào các sinh viên. Sử dụng các đoạn thông tin phía dưới đây để trả lời câu hỏi từ người dùng. Nếu bạn không thể tìm thấy đáp án từ đoạn thông tin, hãy phản hồi: Rất Xin lỗi, tôi không thể tìm thấy thông tin phù hợp để trả lời câu hỏi của bạn. Xin vui lòng liên hệ với văn phòng khoa hoặc văn phòng nhà trường để được giải quyết.

Danh sách thông tin:
{source_knowledge}
""",
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
    def get_rag(self, user_query, chat_history : list):
        ai_response = self.__chain.invoke({
            'messages' : chat_history,
            'source_knowledge':"\n\n".join([item.page_content for item in self.retrieve(user_query)])
        })
        return ai_response
    
    def retrieve(self, user_query : str, top_k : int = 5):
        retrieve_doc = self.__vectorstore.similarity_search(user_query, k=top_k)
        return retrieve_doc