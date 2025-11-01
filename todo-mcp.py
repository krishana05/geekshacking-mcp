from fastmcp import FastMCP
from typing import Annotated
from pydantic import BaseModel
from todo_db import TodoDB

# Create the DB
todo_db = TodoDB()
# todo_db.sample_data()

# Todo class
class Todo(BaseModel):
    filename: str
    text: str
    line_num: int

# Create the MCP server
mcp = FastMCP('TODO-MCP')

# Tools
@mcp.tool(
        name="tool_add_todo",
        description="Add a single #TODO text from a source file"
)
def add_todo(
        filename: Annotated[str, 'Source file name containing #TODO'],
        text: Annotated[str, 'Source file text containing #TODO'],
        line_num: Annotated[int, 'Source file line num containing #TODO']
):
    return todo_db.add(filename, text, line_num)

@mcp.tool(
    name="tool_add_todos",
    description="Add all the #TODO text from a source file"
)
def add_todos(todos: list) -> int:
    """Accepts a list of {filename, text, line_num} objects."""
    for todo_data in todos:
        todo = Todo(**todo_data)
        todo_db.add(todo.filename, todo.text, todo.line_num)
    return len(todos)


# Resource
@mcp.resource(
        name="resource_get_tots_for_file",
        description="Get all todos from a file. Returns an empty array if source file does not exist.",
        uri="todo://{filename}/todos"
)
def get_todos_for_file(filename: Annotated[str, 'Source file conataining #TODO']) -> list[str]:
    todos = todo_db.get(filename)
    return [ text for text in todos.values() ]



# Start the MCP
def main():
    mcp.main()

if __name__ == "__main__":
    main()