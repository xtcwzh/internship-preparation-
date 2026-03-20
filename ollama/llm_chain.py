from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

SYSTEM_PROMPT = """你是一个专业的算法题解析助手。你的职责是：
1. 分析用户提供的算法题目，给出清晰的解题思路
2. 提供时间复杂度和空间复杂度分析
3. 给出 Python 代码实现，并附带关键步骤的注释
4. 如果用户的代码有 bug，帮助找出并修复
5. 对于经典算法（排序、搜索、动态规划、贪心、回溯等），解释其核心思想

回答要求：
- 使用中文回答
- 先分析思路，再给代码
- 代码使用 Python 实现
- 如果用户的问题与算法无关，礼貌地引导回算法话题"""

llm = ChatOllama(model="qwen", temperature=0.3) #ChatOllama 的底层做的事情是：向 http://localhost:11434/api/chat 发送 HTTP 请求，把你的消息传给本地运行的 Ollama 服务。

prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    MessagesPlaceholder(variable_name="history"),#MessagesPlaceholder 是一个占位符，表示历史消息，"对话记忆"的本质 —— 不是模型真的记住了，而是每次把历史消息全部重新发一遍。


    ("human", "{input}"),
])

chain = prompt | llm

# session_id -> list of messages
chat_histories: dict[str, list] = {}


def get_history(session_id: str) -> list:
    return chat_histories.setdefault(session_id, [])


def add_message(session_id: str, role: str, content: str):
    history = get_history(session_id)
    if role == "human":
        history.append(HumanMessage(content=content))
    else:
        history.append(AIMessage(content=content))
    # 只保留最近 20 轮对话，防止上下文过长
    if len(history) > 40:
        chat_histories[session_id] = history[-40:]


async def stream_chat(session_id: str, user_input: str):
    """异步流式生成回复，逐 token yield"""
    history = get_history(session_id)
    add_message(session_id, "human", user_input)

    full_response = ""
    async for chunk in chain.astream({"input": user_input, "history": history[:-1]}):
        token = chunk.content
        if token:
            full_response += token
            yield token

    add_message(session_id, "ai", full_response)
