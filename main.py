from fastmcp import FastMCP
from app.expense_tools import register_tools
from app.desktop_tools import desktop_tools_func

mcp = FastMCP("ExpenseTracker")

register_tools(mcp)
desktop_tools_func(mcp)

# if __name__=="__main__":
#     mcp.run()

