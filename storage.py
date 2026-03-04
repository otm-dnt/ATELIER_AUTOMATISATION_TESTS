import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("runs.sqlite3")

def init_db():
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ts TEXT NOT NULL,
            api_name TEXT NOT NULL,
            avg_ms REAL NOT NULL,
            p95_ms REAL NOT NULL,
            passed INTEGER NOT NULL,
            failed INTEGER NOT NULL
        )
        """)
        con.commit()

def save_run(ts: str, api_name: str, avg_ms: float, p95_ms: float, passed: int, failed: int):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
        INSERT INTO runs(ts, api_name, avg_ms, p95_ms, passed, failed)
        VALUES(?,?,?,?,?,?)
        """, (ts, api_name, avg_ms, p95_ms, passed, failed))
        con.commit()

def list_runs(limit: int = 50):
    init_db()
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        cur = con.execute("SELECT * FROM runs ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(r) for r in cur.fetchall()]
