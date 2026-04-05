from langchain_community.embeddings import DashScopeEmbeddings

embeddings = DashScopeEmbeddings()

print(len(embeddings.embed_query("你好,你能做什么?")))
doc_vecs = embeddings.embed_documents(
    ["你好,你能做什么?", "锄禾日当午，汗滴禾下土.谁知盘中餐，粒粒皆辛苦。"]
)
print(len(doc_vecs),"\n" ,len(doc_vecs[0]))