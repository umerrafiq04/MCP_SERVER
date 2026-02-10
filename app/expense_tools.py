
from fastmcp import FastMCP
from pathlib import Path
mcp = FastMCP("Demo 🚀")
import sqlite3
BASE_DIR = Path(__file__).parent.resolve()
import json
DB_PATH = BASE_DIR / "expenses.db"
CATEGORIES_PATH = BASE_DIR / "categories.json"
print(f"database:{DB_PATH}")
def register_tools(mcp):
    @mcp.tool()
    def test_tool(message: str) -> str:
        return f"Echo: {message}"
    
    @mcp.tool()
    def add_expense(date: str, amount: float, category: str, subcategory: str = "", note: str = ""):
        """Add a new expense to the database"""
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.execute(
                "INSERT INTO expenses (date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
                (date, amount, category, subcategory, note)
            )
            conn.commit()
            return {"status": "success", "id": cur.lastrowid}

    @mcp.tool()
    def list_expenses(start_date: str, end_date: str):
        """List expenses between two dates"""
        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute(
                "SELECT * FROM expenses WHERE date BETWEEN ? AND ? ORDER BY date DESC",
                (start_date, end_date)
            )
            return [dict(row) for row in cur.fetchall()]

    @mcp.tool()
    def summarize(start_date: str, end_date: str, category: str | None = None):
        """Summarize expenses by category"""
        query = """
            SELECT category, SUM(amount) AS total_amount, COUNT(*) AS count
            FROM expenses
            WHERE date BETWEEN ? AND ?
        """
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category"

        with sqlite3.connect(DB_PATH) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.execute(query, params)
            return [dict(row) for row in cur.fetchall()]

    @mcp.tool()
    def delete_item(date: str | None = None, subcategory: str | None = None):
        """Delete expenses by date and/or subcategory"""
        if not date and not subcategory:
            return {"status": "error", "message": "Provide date or subcategory"}

        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            if date and subcategory:
                cur.execute("DELETE FROM expenses WHERE date=? AND subcategory=?", (date, subcategory))
            elif date:
                cur.execute("DELETE FROM expenses WHERE date=?", (date,))
            else:
                cur.execute("DELETE FROM expenses WHERE subcategory=?", (subcategory,))
            conn.commit()

            return {"deleted": cur.rowcount}

    @mcp.resource("expense:///categories")
    def categories() -> str:
        """Get available expense categories"""
        if CATEGORIES_PATH.exists():
            return CATEGORIES_PATH.read_text()
        return json.dumps({
            "categories": [
                "Food", "Transport", "Shopping", "Bills",
                "Healthcare", "Travel", "Education", "Other"
            ]
        }, indent=2)
