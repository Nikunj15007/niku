from pathlib import Path
import sqlite3

DB_PATH = Path(__file__).parent / "cinematch.db"


class Database:
    def __init__(self, path=DB_PATH):
        self.path = str(path)
        self._setup()

    def _connect(self):
        return sqlite3.connect(self.path)

    def _setup(self):
        with self._connect() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS favorites (title TEXT PRIMARY KEY, added_at TEXT DEFAULT CURRENT_TIMESTAMP)")
            conn.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, selected_at TEXT DEFAULT CURRENT_TIMESTAMP)")

    def add_favorite(self, title):
        with self._connect() as conn:
            conn.execute("INSERT OR IGNORE INTO favorites(title) VALUES (?)", (title,))

    def remove_favorite(self, title):
        with self._connect() as conn:
            conn.execute("DELETE FROM favorites WHERE title = ?", (title,))

    def is_favorite(self, title):
        with self._connect() as conn:
            return conn.execute("SELECT 1 FROM favorites WHERE title = ?", (title,)).fetchone() is not None

    def get_favorites(self):
        with self._connect() as conn:
            return [row[0] for row in conn.execute("SELECT title FROM favorites ORDER BY added_at DESC")]

    def add_history(self, title):
        with self._connect() as conn:
            conn.execute("INSERT INTO history(title) VALUES (?)", (title,))

    def get_history(self, limit=20):
        with self._connect() as conn:
            return conn.execute("SELECT title, selected_at FROM history ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
