from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

# 方式1：直接通过 ChatPromptTemplate.from_messages 创建多轮聊天提示词模板
# 传入一个消息列表，每个元素代表一轮消息，格式为（消息类型, 消息内容）
# 消息类型支持：system、human、ai；内容里用 {变量名} 占位，invoke 时再传入

chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Your name is {name}."),
    ("human", "最近怎么样"),
    ("ai", "我很好谢谢"),
    ("human", "{user_input}"),
])

message = chat_template.invoke({"name":"小黄","user_input":"最近怎么样"})
print(message)

# ====================== 方式2：先构建单条消息模板，再组合成聊天模板 ======================
# 依赖包：langchain-core（模块 langchain_core.prompts）
# 类/方法：SystemMessagePromptTemplate.from_template、HumanMessagePromptTemplate.from_template、
#         ChatPromptTemplate.from_messages；填入变量可用 format_messages 或 invoke

system_template_2 = SystemMessagePromptTemplate.from_template(
    "你是一个{role}，请用{language}回答"
)

user_template_2 = HumanMessagePromptTemplate.from_template("{question}")

chat_template_2 = ChatPromptTemplate.from_messages(
    [system_template_2, user_template_2]
)

message_2 = chat_template_2.format_messages(
    role="助手",
    language="中文",
    question="你最喜欢什么?",
)
# 等价写法：message_2 = chat_template_2.invoke({"role": "助手", "language": "中文", "question": "你最喜欢什么?"})

print(message_2)
