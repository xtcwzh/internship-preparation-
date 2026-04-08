from langchain.agents import create_agent
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_core.tools import tool

@tool(description="这是一个工具，用于获取天气信息")
def get_weather():
    return "晴天"

agent = create_agent(
    model = ChatTongyi(model = "qwen3-max"),
    tools = [get_weather],
    system_prompt = "你是一个天气助手，用于获取天气信息",
)


res = agent.invoke(
    {
        "messages": [
            {"role": "user", "content": "今天苏州天气怎么样"}
        ]
    }
)

for mes in res["messages"]:
    print(type(mes).__name__,mes.content)



