import sqlite3
from pathlib import Path
from models.phrase import Phrase
from datetime import datetime

DB_PATH = Path.home() / ".phrase_manager" / "phrases.db"

class Database:
    def __init__(self):
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS phrases (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                title       TEXT NOT NULL,
                content     TEXT NOT NULL,
                category    TEXT DEFAULT 'عمومی',
                tags        TEXT DEFAULT '',
                created_at  TEXT,
                updated_at  TEXT
            )
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """)
        # دسته‌بندی‌های پیش‌فرض
        defaults = [("عمومی",), ("کاری",), ("شخصی",), ("برنامه‌نویسی",)]
        self.conn.executemany(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)", defaults
        )
        self.conn.commit()

    # ─── CRUD ────────────────────────────────────────────

    def add_phrase(self, phrase: Phrase) -> int:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cur = self.conn.execute(
            """INSERT INTO phrases (title, content, category, tags, created_at, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (phrase.title, phrase.content, phrase.category,
             phrase.tags, now, now)
        )
        self.conn.commit()
        return cur.lastrowid

    def update_phrase(self, phrase: Phrase):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(
            """UPDATE phrases
               SET title=?, content=?, category=?, tags=?, updated_at=?
               WHERE id=?""",
            (phrase.title, phrase.content, phrase.category,
             phrase.tags, now, phrase.id)
        )
        self.conn.commit()

    def delete_phrase(self, phrase_id: int):
        self.conn.execute("DELETE FROM phrases WHERE id=?", (phrase_id,))
        self.conn.commit()

    def get_all(self, category: str = None, search: str = "") -> list[Phrase]:
        query = "SELECT * FROM phrases WHERE 1=1"
        params = []

        if category and category != "همه":
            query += " AND category=?"
            params.append(category)

        if search:
            query += " AND (title LIKE ? OR content LIKE ? OR tags LIKE ?)"
            like = f"%{search}%"
            params.extend([like, like, like])

        query += " ORDER BY updated_at DESC"
        rows = self.conn.execute(query, params).fetchall()
        return [Phrase(**dict(row)) for row in rows]

    def get_categories(self) -> list[str]:
        rows = self.conn.execute("SELECT name FROM categories ORDER BY name").fetchall()
        return ["همه"] + [r["name"] for r in rows]

    def add_category(self, name: str):
        self.conn.execute(
            "INSERT OR IGNORE INTO categories (name) VALUES (?)", (name,)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()
