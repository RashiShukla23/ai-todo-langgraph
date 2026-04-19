from dotenv import load_dotenv
from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.postgres import PostgresSaver
from tools import add_todo, delete_todo, search_todos, get_all_todos
from db import get_connection, create_table
import psycopg
import os

load_dotenv()

tools = [add_todo, delete_todo, search_todos, get_all_todos]

class State(TypedDict):
    messages: Annotated[list, add_messages]

llm = init_chat_model(model_provider="openai", model="gpt-4.1")
llm_with_tools = llm.bind_tools(tools)

def chatbot(state: State):
    message = llm_with_tools.invoke(state["messages"])
    return {"messages": [message]}

tool_node = ToolNode(tools=tools)

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", tool_node)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

DB_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

connection = psycopg.connect(DB_URI, autocommit=True)
checkpointer = PostgresSaver(connection)
checkpointer.setup()

graph = graph_builder.compile(checkpointer=checkpointer)

def main():
    create_table()
    thread_id = input("Enter your session ID (any name/number): ")
    config = {"configurable": {"thread_id": thread_id}}
    
    print(f"\nSession '{thread_id}' started! Type your message:\n")
    
    while True:
        user_query = input("> ")
        
        if user_query.lower() == "exit":
            break

        state = State(
            messages=[{"role": "user", "content": user_query}]
        )

        for event in graph.stream(state, config, stream_mode="values"):
            if "messages" in event:
                last_message = event["messages"][-1]
                print(f"\n{last_message.type.upper()}: {last_message.content}\n")

main()