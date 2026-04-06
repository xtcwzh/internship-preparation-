from langchain_community.chat_models import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.runnables import RunnableLambda, RunnablePassthrough
from vector_stores import VectorStores
import config_data as config
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from typing import List
from file_history_store import get_history
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_core.prompts import MessagesPlaceholder

def print_prompt(prompt):

    print("="*100,prompt.to_string())

    return prompt

class RagService(object):
    def __init__(self):

        self.vertor_service = VectorStores(embedding = DashScopeEmbeddings(model=config.embedding_model_name))

        self.prompt = ChatPromptTemplate.from_messages([
            ("system","以我提供的已知参考资料为主，简洁专业的回答问题。参考资料:{context}"),
            ("system","并且我提供如下历史记录"),
            MessagesPlaceholder("history"),
            ("human","请回答用户提问:{input}")
        ])

        self.chat_model = ChatTongyi(model=config.chat_model_name)

        self.chain = self.__get_chain()

    
    def __get_chain(self):
        retriever = self.vertor_service.get_retriver()

        def format_docs(docs:List[Document]):
            if not docs:
                return "无相关参考资料"
            
            formatted_str = "["

            for doc in docs:
                formatted_str += f"来源: {doc.metadata.get('source', '未知来源')}\n内容: {doc.page_content}\n\n"

            formatted_str += "]"

            return formatted_str
        def format_for_retriever(value):
            return value["input"]

        def format_for_prompt(value):
            new_value = {}
            new_value["input"] = value["input"]["input"]
            new_value["history"] = value["input"]["history"]
            new_value["context"] = value["context"]
            return new_value

        chain = {
            "input":RunnablePassthrough(),
            "context":RunnableLambda(format_for_retriever)|retriever | format_docs,
        } | RunnableLambda(format_for_prompt) | self.prompt | print_prompt |self.chat_model|StrOutputParser()

        conversation_chain = RunnableWithMessageHistory(
            chain,
            get_history,
            input_messages_key="input",
            history_messages_key="history",
        )

        return conversation_chain

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }
    rag_service = RagService()
    result = rag_service.chain.invoke({"input":"春天穿什么衣服"},session_config)
    print(result)

