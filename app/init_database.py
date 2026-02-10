import sqlite3
from pathlib import Path
import sqlite3
BASE_DIR = Path(__file__).parent.resolve()
import json
DB_PATH = BASE_DIR / "expenses.db"
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)
        conn.commit()

# ✅ Initialize DB at module level
init_db()