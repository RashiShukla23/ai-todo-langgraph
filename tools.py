from langchain_core.tools import tool
from db import get_connection

@tool()
def add_todo(task: str):
    """Adds a new todo task to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id", (task,))
    todo_id = cursor.fetchone()[0]
    conn.commit()
    cursor.close()
    conn.close()
    return f"Task added successfully with ID {todo_id}"

@tool()
def delete_todo(task_id: int):
    """Deletes a todo task from the database by its ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s RETURNING id", (task_id,))
    deleted = cursor.fetchone()
    conn.commit()
    cursor.close()
    conn.close()
    if deleted:
        return f"Task {task_id} deleted successfully"
    return f"Task {task_id} not found"

@tool()
def search_todos(keyword: str):
    """Searches for todo tasks containing the keyword"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, created_at FROM todos WHERE task ILIKE %s", (f"%{keyword}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        return "No tasks found"
    return "\n".join([f"ID: {row[0]} | Task: {row[1]} | Added: {row[2]}" for row in results])

@tool()
def get_all_todos():
    """Returns all todo tasks from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, task, created_at FROM todos")
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    if not results:
        return "No tasks found"
    return "\n".join([f"ID: {row[0]} | Task: {row[1]} | Added: {row[2]}" for row in results])