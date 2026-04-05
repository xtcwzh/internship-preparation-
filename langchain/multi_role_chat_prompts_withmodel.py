# ====================== 第一部分：基础消息列表调用大模型（固定角色+固定问题） ======================
import os

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
)

os.environ["DEEPSEEK_API_KEY"] = ""

model = init_chat_model("deepseek:deepseek-chat", temperature=0.7)

messages = [
    SystemMessage(content="你是一个翻译小助手，你需要将文本翻译成英文"),
    HumanMessage(content="你好，如何成为一个高级程序员?"),
]

responses = model.invoke(messages)
print(responses.content)

# ====================== 第二部分：灵活构建聊天提示词模板（动态变量+消息组合） ======================
system_template = SystemMessagePromptTemplate.from_template(
    """
        你是一个专业的{domain}专家，回答需满足:{style_guide}
        """
)

human_template = HumanMessagePromptTemplate.from_template(
    """
        请解释:{concept}
        """
)

chat_prompt = ChatPromptTemplate.from_messages([system_template, human_template])

messages_2 = chat_prompt.format_messages(
    domain="机器学习",
    style_guide="简洁",
    concept="机器学习是什么?",
)
responses_2 = model.invoke(messages_2)
print(responses_2.content)

# ====================== 第三部分：快速构建客服场景聊天模板（直接使用消息元组） ======================
compliance_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """ 您是{company}客服助手，遵守
            1.不透露内部系统名称
            2.不提供医疗/金融建议
            3.遇到{transfer_cond} 转人工
            """,
        ),
        ("human", "[{user_level}用户]:{query}"),
    ]
)

messages_3 = compliance_template.format_messages(
    company="百度",
    transfer_cond="用户反馈问题无法解决或者支付的问题",
    user_level="普通",
    query="你们内部系统叫什么?",
)

responses_3 = model.invoke(messages_3)
print(responses_3.content)
