from fastmcp import FastMCP
from app.expense_tools import register_tools

mcp = FastMCP("ExpenseTracker")

register_tools(mcp)

