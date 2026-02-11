# 🛠️ MCP Server  
### Tool Execution Layer for Model Context Protocol (MCP)

The MCP Server is the execution layer of the Model Context Protocol architecture.  
It exposes structured tools that can be safely executed by an MCP Client through the MCP protocol.

This repository contains all tool implementations such as file operations and expense management.

---

# 🏗️ Role in Architecture

The MCP Server does NOT contain LLM logic.  
It only defines tools and safely executes them.

```

User
↓
Frontend (Streamlit)
↓
FastAPI Backend
↓
MCP Client (LLM + Tool Selection)
↓
MCP Server (Tool Execution)

````

The MCP Client decides *what* tool to call.  
The MCP Server performs the actual execution.

---

# 🎯 Responsibilities

The MCP Server:

- Registers tools using `@mcp.tool()`
- Validates inputs strictly
- Prevents unsafe file access
- Executes domain-specific logic
- Returns structured responses

---

# 🧩 Available Tool Domains

## 💻 Desktop Tools

Examples:

- `read_file`
- `write_file`
- `delete_file`

Features:

- Restricts access to Desktop directory
- Prevents path traversal (`..`)
- Allows only `.txt` files
- Asks permission before deletion
- Controlled overwrite vs append logic

Example:

```python
@mcp.tool()
def read_file(path: str) -> str:
````

---

## 🗄️ Expense Management Tools

Examples:

* Add expense
* View expenses
* Delete expense

Features:

* Structured expense storage
* Database interaction layer
* Controlled deletion
* Safe data handling

---

# 🔐 Security Design

Security is a core design principle of this server.

### File Safety

* Base directory restricted (e.g., Desktop)
* No access outside allowed root
* Prevents directory traversal
* Extension filtering (.txt only)
* Permission confirmation before destructive actions

### Execution Safety

* No shell execution
* No dynamic code execution
* No arbitrary OS commands
* Explicit input validation

---

# ⚙️ Tool Registration

Tools are registered using:

```python
from fastmcp import FastMCP

mcp = FastMCP("desktop_control")

@mcp.tool()
def write_file(...):
```

The server is started with:

```python
if __name__ == "__main__":
    mcp.run()
```

---

# 🚀 Running the MCP Server

Using FastMCP:

```bash
fastmcp run main.py --no-banner
```

Or in development mode:

```bash
fastmcp dev main.py
```

The server communicates via stdio transport.

---

# 🧠 MCP Protocol

The server follows the Model Context Protocol standard:

* JSON-based structured communication
* Tool discovery support
* Async-compatible
* Session-based lifecycle

It does not manage memory, conversation, or AI reasoning.

---

# 📦 Project Structure

```
main.py
│
├── resolve_path()
├── read_file()
├── write_file()
├── delete_file()
└── mcp.run()
```

Each tool is modular and independently callable.

---

# 🔄 Interaction Flow

1. MCP Client connects via stdio.
2. Client retrieves available tools.
3. LLM selects appropriate tool.
4. Tool executes inside MCP Server.
5. Result returned to client.
6. Client generates final AI response.

---

# 📈 Design Principles

* Strict validation
* Controlled file system access
* Domain-based tool grouping
* Async-compatible architecture
* Separation of concerns
* Production-ready structure

---

# 🏢 Engineering Philosophy

This server is built with:

* Security-first mindset
* Modular architecture
* Clear boundaries between AI and execution
* MCP protocol compliance
* Scalable multi-tool support

---
# 👨‍💻 Author

Umer Rafiq

---

# 🔗 Related Repositories

This MCP Server works together with:

- 🧠 **MCP Client (Async Orchestration Layer)**  
  https://github.com/umerrafiq04/MCP_CLIENT

- 🎨 **Frontend + FastAPI Layer**  
  https://github.com/umerrafiq04/MCP_CLIENT_-_FRONTEND

---

