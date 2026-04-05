# from langchain_community.llms import Tongyi

# model = Tongyi(model="qwen-max")

# res = model.invoke("你好")

# print(res)


from langchain_ollama import OllamaLLM

model = OllamaLLM(model="qwen3:4b")

res = model.invoke("你好")

print(res)