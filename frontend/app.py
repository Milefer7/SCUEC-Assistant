# frontend/app.py

import streamlit as st
import requests


# 定义向后端发送请求的函数
def call_api(query):
    url = "http://localhost:8000/query"  # FastAPI 的地址
    payload = {"query": query}
    response = requests.post(url, json=payload)
    return response.json()['answer']


# Streamlit 用户界面
st.title("RAG Model Query Interface")

# 创建一个对话框记录对话内容
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

if query:
    # 将用户输入添加到会话历史
    st.session_state['messages'].append({"role": "user", "content": query})

    # 调用API获取回答
    response = call_api(query)

    # 将回答添加到会话历史
    st.session_state['messages'].append({"role": "answer", "content": response})

    # 自动刷新页面，显示最新的对话
    st.session_state['messages'] = st.session_state['messages']
