from langchain_chroma import Chroma
import config_data as config

class VectorStores(object):

    def __init__(self,embedding):
        self.embedding = embedding
        self.vector_store = Chroma(
            collection_name=config.collection_name,
            embedding_function=self.embedding,
            persist_directory=config.persist_directory,
        )
    
    def get_retriver(self):
        return self.vector_store.as_retriever(
            search_kwargs={"k": config.similarity_threshold}
        )

if __name__ == "__main__":
    from langchain_community.embeddings import DashScopeEmbeddings    
    embedding = DashScopeEmbeddings(model="text-embedding-v4")
    vector_stores = VectorStores(embedding)
    retriever = vector_stores.get_retriver()
    print(retriever.invoke("我身高180，体重70kg，我应该选什么码的衣服"))
        