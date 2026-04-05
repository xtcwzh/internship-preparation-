from langchain_community.llms import Tongyi

model = Tongyi(model="qwen-max")

res = model.stream("你好,你能做什么?")

for chunk in res:
    print(chunk,end="",flush=True)