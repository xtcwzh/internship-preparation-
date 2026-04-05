import os,json
from typing import Sequence

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import PromptTemplate,MessagesPlaceholder,ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import message_to_dict,messages_from_dict,BaseMessage

model = ChatTongyi(model="qwen3-max")

class FileChatMessageHistory:
    def __init__(self,session_id,storage_path):
        self.session_id = session_id
        self.storage_path = storage_path
        self.storage_path = os.path.join(self.storage_path,self.session_id)

        os.makedirs(os.path.dirname(self.storage_path),exist_ok=True)
    
    def add_messages(self,messages:Sequence[BaseMessage]):
        all_messages = list(self.messages)
        all_messages.extend(messages)

        # json 只能序列化 list/dict 等，不能写生成器；否则 dump 失败会留下空文件，下次 load 报错
        payload = [message_to_dict(m) for m in all_messages]
        with open(self.storage_path,"w",encoding="utf-8") as f:
            json.dump(payload, f, ensure_ascii=False)

    @property
    def messages(self) -> Sequence[BaseMessage]:
        try:
            with open(self.storage_path,"r",encoding="utf-8") as f:
                raw = f.read().strip()
                if not raw:
                    return []
                return messages_from_dict(json.loads(raw))
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []
    
    def clear_messages(self):
        with open(self.storage_path,"w",encoding="utf-8") as f:
            json.dump([],f)



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


def get_history(session_id):
    return FileChatMessageHistory(session_id,storage_path="/Users/wangzihao/Documents/实习资料/project preparation for internship/RAG_Agent/P3_langchain_RAG")

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
    # res = conversation_chain.invoke({"input":"小明有两只猫"},session_config)
    # print(res)

    # res = conversation_chain.invoke({"input":"小红有一只狗"},session_config)
    # print(res)

    res = conversation_chain.invoke({"input":"一共有几只宠物"},session_config)
    print(res)