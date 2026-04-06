import streamlit as st
import time
from rag import RagService
import config_data as config
st.title("智能客服")
st.divider()

if "rag_service" not in st.session_state:
    st.session_state.rag_service = RagService()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role":"assitant","content":"你好，我是你的智能客服，有什么可以帮你的吗？"}]

for message in st.session_state["messages"]:
    st.chat_message(message["role"]).write(message["content"])


prompt = st.chat_input()

if prompt:

    st.chat_message("user").write(prompt)
    st.session_state.messages.append({"role":"user","content":prompt})

    ai_res_list = []
    with st.spinner("AI思考中..."):
        result_stream = st.session_state["rag_service"].chain.stream({"input":prompt},config.session_config)
        
        def capture(generator,cache_list):
            for chunk in generator:
                cache_list.append(chunk)
                yield chunk
        
        st.chat_message("assistant").write_stream(capture(result_stream,ai_res_list))
        st.session_state.messages.append({"role":"assistant","content":"".join(ai_res_list)})