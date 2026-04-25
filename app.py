import streamlit as st
from graph import graph, State
import uuid

st.set_page_config(page_title="AI Todo List", page_icon="</>")
st.title("AI Powered To-Do List")
st.caption("Chat with your AI assistant to manage your tasks!")

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

if prompt := st.chat_input("Type your task or question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    state = State(
        messages=[{"role": "user", "content": prompt}]
    )

    config = {"configurable": {"thread_id": st.session_state.thread_id}}

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            final_response = ""
            for event in graph.stream(state, config, stream_mode="values"):
                if "messages" in event:
                    last_message = event["messages"][-1]
                    if last_message.type == "ai" and last_message.content:
                        final_response = last_message.content
            st.write(final_response)

    st.session_state.messages.append({"role": "assistant", "content": final_response})