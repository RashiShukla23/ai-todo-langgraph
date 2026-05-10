# AI To-Do List Agent

A conversational to-do list app where you manage tasks through natural language. Just type what you want and the agent handles the rest.

---

## What it does

- Add, update, delete, and list tasks by chatting naturally
- Remembers tasks across sessions using PostgreSQL
- Tracks conversation state per session with psycopg3 checkpointing
- Monitors agent runs through LangSmith tracing

---

## Tech Stack

| Layer | Technology |
|---|---|
| LLM | GPT-4.1 (OpenAI) |
| Agent Framework | LangGraph |
| Frontend | Streamlit |
| Database | PostgreSQL |
| DB Driver | psycopg3 |
| Monitoring | LangSmith |
| Language | Python |

---

## Project Structure

```
ai-todo-langgraph/
├── app.py       # Streamlit UI and session management
├── graph.py     # LangGraph agent graph
├── tools.py     # Task tools (add, delete, update, list)
├── db.py        # PostgreSQL connection and queries
└── .gitignore
```

---

## Getting Started

Prerequisites: Python 3.10+, PostgreSQL, OpenAI API key

```bash
git clone https://github.com/RashiShukla23/ai-todo-langgraph.git
cd ai-todo-langgraph

py -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file:

```
OPENAI_API_KEY=your_key
LANGSMITH_API_KEY=your_key
DATABASE_URL=postgresql://user:password@localhost:5432/todo_db
```

```bash
streamlit run app.py
```

---

## How it works

The user sends a message, the LangGraph agent decides which tool to call (add/update/delete/list), the tool runs the corresponding PostgreSQL query, and the assistant replies. Conversation state is checkpointed per session so context is never lost.

---

## Example

```
You: Add "submit assignment" to my tasks
Agent: Done! Added "submit assignment" to your list.

You: Show all tasks
Agent: Here's what you have:
  1. submit assignment
  2. buy groceries

You: Delete buy groceries
Agent: Removed "buy groceries".
```

---

## Author

**Rashi Shukla** — [GitHub](https://github.com/RashiShukla23)
