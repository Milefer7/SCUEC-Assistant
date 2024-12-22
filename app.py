import asyncio
import streamlit as st
from be.controller.query import websocket_communicate  # 假设这是你用来进行 WebSocket 通信的函数

# Streamlit 用户界面
st.title("SCUEC Chatbot", anchor="top")

# 用于存储聊天历史记录
if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# 自定义CSS样式，用于美化聊天界面
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f7f7f7;
        margin: 0;
        padding: 0;
    }
    .user-message {
        background-color: #D1E7FF;
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 12px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 16px;
        margin-left: auto;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .answer-message {
        background-color: #F1F1F1;
        border-radius: 15px;
        padding: 12px;
        margin-bottom: 12px;
        max-width: 80%;
        word-wrap: break-word;
        font-size: 16px;
        margin-right: auto;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .message-container {
        display: flex;
        flex-direction: column;
        margin-bottom: 20px;
    }
    .input-container {
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        margin-top: 20px;
    }
    .stTextInput input {
        padding: 10px;
        border-radius: 12px;
        border: 1px solid #ccc;
        font-size: 16px;
        width: 100%;
        max-width: 600px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        border: none;
        border-radius: 8px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton button:hover {
        background-color: #45a049;
    }
    .sidebar {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
        height: 100%;
        padding: 20px;
        justify-content: flex-start;
    }
    .chat-container {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        padding: 20px;
    }
    .messages-column {
        flex: 0.7;
        padding-right: 20px;
        overflow-y: auto;
        height: 70vh;
        max-width: 700px;
    }
    .input-column {
        flex: 0.3;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        height: 70vh;
        overflow-y: auto;
    }
    </style>
""", unsafe_allow_html=True)

# 创建页面布局：分栏
col1, col2 = st.columns([7, 3])

# 左侧为聊天记录区域
with col1:
    # 显示历史消息
    st.markdown("### Chat History")
    for message in st.session_state['messages']:
        with st.container():
            if message['role'] == 'user':
                st.markdown(f'<div class="message-container"><div class="user-message">{message["content"]}</div></div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="message-container"><div class="answer-message">{message["content"]}</div></div>', unsafe_allow_html=True)

# 右侧为输入区域
with col2:
    # 清除聊天记录按钮
    if st.button("Clear Chat"):
        st.session_state['messages'] = []

    # 输入框
    st.markdown("### Ask a Question")
    query = st.text_input("Enter your question:", key="query", max_chars=500)

    # 提交按钮
    if st.button("Send"):
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
