import asyncio

import streamlit as st
from be.controller.query import *

# Streamlit 用户界面
st.title("SCUEC Chatbot")

# 用于存储聊天历史记录
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# 显示历史消息
for message in st.session_state['messages']:
    if message['role'] == 'user':
        st.markdown(f"**User:** {message['content']}")
    else:
        st.markdown(f"**Answer:** {message['content']}")


# 用户输入框
query = st.text_input("Ask a question:")
# print(query)

# WebSocket连接的异步事件监听
if query:
    # 将用户输入添加到会话历史
    st.session_state['messages'].append({"role": "user", "content": query})

    # 定义一个异步函数来循环监听和更新聊天内容
    async def listen_and_respond():
        response = await websocket_communicate(query)  # 发送并接收消息
        # 将回答添加到会话历史
        st.session_state['messages'].append({"role": "answer", "content": response})


    # 使用 asyncio 运行事件循环监听 WebSocket
    asyncio.run(listen_and_respond())

    # 显示更新后的对话
    st.session_state['messages'] = st.session_state['messages']
