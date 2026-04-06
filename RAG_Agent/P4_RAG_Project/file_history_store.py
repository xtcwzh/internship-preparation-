import os
import json
from typing import Sequence
from langchain_core.messages import BaseMessage
from langchain_core.messages import message_to_dict, messages_from_dict

def get_history(session_id):
    return FileChatMessageHistory(session_id,storage_path="/Users/wangzihao/Documents/实习资料/project preparation for internship/RAG_Agent/P4_RAG_Project")

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