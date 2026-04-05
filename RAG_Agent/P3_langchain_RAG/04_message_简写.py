from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

model = ChatTongyi(model="qwen3-max")

messages = [
    ("system","你是一个边塞诗人."),
    ("user","写一首诗."),
    ("assistant","锄禾日当午，汗滴禾下土.谁知盘中餐，粒粒皆辛苦。"),
    ("user","模拟之前的诗句，再写一首诗")
]

res = model.stream(messages)

for chunk in res:
    print(chunk.content,end=" ",flush=True)