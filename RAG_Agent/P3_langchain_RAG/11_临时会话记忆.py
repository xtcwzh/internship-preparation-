from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate,MessagesPlaceholder,ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory

model = ChatTongyi(model="qwen3-max")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system","你需要跑根据会话历史回复用户消息，对话历史："),
        MessagesPlaceholder("history"),
        ("human","请回复以下问题:{input}")
    ]
)

str_parser = StrOutputParser()

def print_prompt(full_prompt):
    print("=" * 20,full_prompt.to_string(),"=" * 20)
    return full_prompt

base_chain = prompt |print_prompt| model | str_parser

store = {}

def get_history(session_id):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

conversation_chain = RunnableWithMessageHistory(
    base_chain,
    get_history,
    input_messages_key="input",
    history_messages_key="history",
)

if __name__ == "__main__":
    session_config = {
        "configurable":{
            "session_id":"user_001"
        }
    }
    res = conversation_chain.invoke({"input":"小明有两只猫"},session_config)
    print(res)

    res = conversation_chain.invoke({"input":"小红有一只狗"},session_config)
    print(res)

    res = conversation_chain.invoke({"input":"一共有几只宠物"},session_config)
    print(res)

