from langchain_community.chat_models import ChatTongyi
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

chain = my_template |pront_prompt| model |StrOutputParser()

vector_store.add_texts(["减肥就是要少食多餐","减肥要多吃蔬菜","减肥要少吃肉","我喜欢游泳","我是一个研究生"])
input_text = "如何减肥"
result = vector_store.similarity_search(input_text,k=2)

reference_text = "["

for doc in result:
    reference_text += doc.page_content

reference_text += "]"

res = chain.invoke({"context":reference_text,"input":input_text})
print(res)