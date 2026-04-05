from langchain_community.chat_models import ChatTongyi
from langchain_core.runnables import Runnable, RunnablePassthrough
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate



model = ChatTongyi(model="qwen-max")

my_template =  ChatPromptTemplate.from_messages([
    ("system","请回答用户的问题，要求参考知识库{context}"),
    ("human", "{input}")
])

vector_store = InMemoryVectorStore(
    embedding=DashScopeEmbeddings(model="text-embedding-v2"),
)

def pront_prompt(prompt):
    print(prompt.to_string())
    return prompt

input = "如何减肥"

vector_store.add_texts(["减肥就是要少食多餐","减肥要多吃蔬菜","减肥要少吃肉","我喜欢游泳","我是一个研究生"])

retriever = vector_store.as_retriever(search_kwargs={"k": 2})

def format_fun(docs):
    format_doc = f"["
    for doc in docs:
        format_doc += doc.page_content
    format_doc += "]"
    return format_doc

chain = {"input":RunnablePassthrough(),"context":retriever | format_fun}| my_template |pront_prompt| model |StrOutputParser()

result = chain.invoke(input)
print(result)