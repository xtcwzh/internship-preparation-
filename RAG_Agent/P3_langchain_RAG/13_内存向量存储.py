from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.document_loaders import CSVLoader
from pydantic_settings import sources

loader = CSVLoader(
    file_path="./data/info.csv",
    encoding="utf-8",
    source_column = "source"
)

vector_store = InMemoryVectorStore(
    embedding = DashScopeEmbeddings()
)

docs = loader.load()

vector_store.add_documents(documents = docs,ids = ["id" + str(i) for i in range(1,len(docs)+1)])

vector_store.delete(["id1","id2"])

res = vector_store.similarity_search("python值不值得学习",k=2)
print(res)



