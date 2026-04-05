from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain_community.chat_models import ChatTongyi

chat_prompt_temple = ChatPromptTemplate.from_messages([
    ("system","你是一个边塞诗人."),
    MessagesPlaceholder("history"),
    ("user","再写一首诗."),
])

history_data = [
    ("user","写一首诗."),
    ("ai","锄禾日当午，汗滴禾下土.谁知盘中餐，粒粒皆辛苦。"),
    ("user","再写一首诗."),
    ("ai","床前明月光，疑是地上霜。举头望明月，低头思故乡。"),
]

prompt_text = chat_prompt_temple.invoke({"history":history_data})
print(prompt_text.to_string())

model = ChatTongyi(model="qwen-max")
res = model.invoke(prompt_text)
print(res.content)