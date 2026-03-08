# 🛠️ MCP Server  
### Tool Execution Layer for Model Context Protocol (MCP)

The MCP Server is the execution layer of the Model Context Protocol architecture.  
It exposes structured tools that can be safely executed by an MCP Client through the MCP protocol.

This repository contains tool implementations for:

- Desktop file operations
- Expense database management
- PDF document tools

The MCP Server focuses purely on **tool execution and safety**, while the MCP Client handles **LLM reasoning and tool selection**.

---

# 🏗️ Role in Architecture

The MCP Server **does not contain LLM logic**.

Its responsibility is to expose structured tools that can be executed by an MCP Client.

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
```

The MCP Client decides **which tool to call**, and the MCP Server performs the **actual execution**.

---

# 🎯 Responsibilities

The MCP Server:

- Registers tools using `@mcp.tool()`
- Validates inputs strictly
- Restricts file system access
- Prevents unsafe file operations
- Executes domain-specific logic
- Returns structured outputs

The server acts as a **secure execution layer between AI reasoning and real-world operations**.

---

# 📦 Project Structure

The MCP Server follows a **modular tool architecture**, where each domain has its own tool module.

```
MCP_SERVER/
│
├── main.py                # MCP server entry point
│
└── app/
    ├── desktop_tools.py   # Desktop file operations
    ├── expense_tools.py   # Expense tracking tools
    └── pdf_tools.py       # PDF reading and management tools
```

### Architecture Design

- **main.py** initializes the MCP server
- Each module registers its own tools
- Tools are grouped by domain
- The system remains easily extensible

New tool domains can be added simply by creating a new module inside `app/`.

---

# 🧩 Available Tool Domains

The MCP Server exposes three tool domains:

| Domain | Description |
|------|------|
| Desktop Tools | Secure file management on Desktop |
| Expense Tools | Expense tracking and database operations |
| PDF Tools | PDF document reading, searching, and management |

---

# 💻 Desktop Tools

Handles secure file operations on the Desktop.

### Available Tools

- `read_file`
- `write_file`
- `delete_file`
- `list_files`

### Features

- Restricts access to Desktop directory
- Prevents path traversal (`..`)
- Allows only `.txt` files
- Confirmation required before deletion
- Safe overwrite vs append logic

Example:

```python
@mcp.tool()
def read_file(path: str) -> str:
```

---

# 🗄️ Expense Management Tools

Provides structured expense tracking.

### Available Tools

- `add_expense`
- `view_expenses`
- `delete_expense`

### Features

- Structured expense storage
- Database-backed operations
- Controlled deletion
- Safe financial logging

These tools allow AI systems to **track automation costs and financial records**.

---

# 📄 PDF Document Tools

The MCP Server provides advanced **PDF document intelligence tools**.

### Available Tools

- `read_pdf`
- `search_pdf`
- `create_pdf`
- `rename_pdf`
- `delete_pdf`
- `find_relevant_pdfs_on_desktop`

---

## 📖 read_pdf

Reads full text from a PDF file.

Example:

```python
read_pdf("report.pdf")
```

Features:

- Multi-page extraction
- Desktop-only file access
- `.pdf` extension validation

---

## 🔍 search_pdf

Searches a keyword inside a PDF.

Example:

```python
search_pdf("report.pdf", "revenue")
```

Features:

- Page-based search
- Case-insensitive matching
- Limited output size

---

## 🧾 create_pdf

Creates a new PDF file from provided text.

Example:

```python
create_pdf("notes.pdf", "AI systems are evolving rapidly.")
```

Features:

- Automatic `.pdf` extension
- Prevents overwriting existing files
- Uses `reportlab` for PDF generation

---

## ✏️ rename_pdf

Renames a PDF file.

Example:

```python
rename_pdf("report.pdf", "summary.pdf", confirm="RENAME report.pdf")
```

---

## 🗑️ delete_pdf

Deletes a PDF file.

Example:

```python
delete_pdf("report.pdf", confirm="DELETE report.pdf")
```

Deletion requires strict confirmation.

---

## 🔎 find_relevant_pdfs_on_desktop

Searches all PDFs on the Desktop for relevant information.

Example:

```python
find_relevant_pdfs_on_desktop("machine learning")
```

---

# 🔐 Security Design

Security is a **core design principle** of this server.

---

## File System Safety

The server enforces strict filesystem protections:

- Desktop-only access
- Path traversal prevention
- Extension filtering
- Confirmation for destructive actions

---

## PDF Safety

Additional safeguards include:

- `.pdf` extension validation
- Controlled rename and deletion
- No overwrite during creation

---

## Execution Safety

The server prevents unsafe operations:

- No shell execution
- No dynamic code execution
- No arbitrary OS commands

---

# ⚙️ Tool Registration

Tools are registered using **FastMCP**.

Example:

```python
from fastmcp import FastMCP

server = FastMCP("ExpenseTracker")
```

Each tool module registers its tools with the MCP server.

---

# 🚀 Server Initialization

### main.py

```python
from fastmcp import FastMCP

from app.expense_tools import register_tools
from app.desktop_tools import desktop_tools_func
from app.pdf_tools import pdf_tools_func

server = FastMCP("ExpenseTracker")

desktop_tools_func(server)
register_tools(server)
pdf_tools_func(server)

if __name__ == "__main__":
    server.run()
```

This modular initialization enables:

- Domain-based tool separation
- Easier maintenance
- Scalable tool expansion

---

# 🚀 Running the MCP Server

Using FastMCP:

```bash
fastmcp run main.py --no-banner
```

Development mode:

```bash
fastmcp dev main.py
```

The server communicates using **stdio transport**.

---

# 🔄 Interaction Flow

1️⃣ MCP Client connects to the MCP Server.

2️⃣ Client retrieves available tools.

3️⃣ LLM selects the appropriate tool.

4️⃣ Tool executes inside the MCP Server.

5️⃣ Result returned to client.

6️⃣ Client generates final AI response.

---

# 📈 Design Principles

- Modular tool architecture
- Strict input validation
- Controlled filesystem access
- Domain-based tool grouping
- Separation of AI and execution layers
- Production-ready system design

---

# 🏢 Engineering Philosophy

This server is built with:

- Security-first architecture
- Clear separation between reasoning and execution
- MCP protocol compliance
- Scalable multi-tool support
- Clean modular design

---

# 👨‍💻 Author

**Umer Rafiq**

---

# 🔗 Related Repositories

This MCP Server works together with:

### 🎨 Frontend + FastAPI Layer

https://github.com/umerrafiq04/MCP_CLIENT_-_FRONTEND
