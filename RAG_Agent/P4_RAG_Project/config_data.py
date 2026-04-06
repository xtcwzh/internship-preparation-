import os

# 相对本文件目录，避免 streamlit / python 启动时工作目录不同导致找不到文件
_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

md5_path = os.path.join(_BASE_DIR, "md5.text")

collection_name = "rag"

persist_directory = os.path.join(_BASE_DIR, "chroma_db")

chunk_size = 1000
chunk_overlap = 100
separators = ["\n\n", "\n", ".", "!", "?", ",", " ", ""]

max_split_char_number = 1000

similarity_threshold = 1

embedding_model_name = "text-embedding-v4"
chat_model_name = "qwen3-max"

session_config = {
    "configurable":{
        "session_id":"user_001"
    }
}