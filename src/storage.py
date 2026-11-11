import os
import sqlite3
from contextlib import closing
from pathlib import Path

from models import Book


def data_dir() -> Path:
    base = os.getenv("FLET_APP_STORAGE_DATA")
    path = Path(base) if base else Path.home() / ".checkbook"
    path.mkdir(parents=True, exist_ok=True)
    return path


DB_PATH = data_dir() / "books.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _to_book(row: sqlite3.Row) -> Book:
    return Book(
        id=row["id"], title=row["title"], author=row["author"],
        status=row["status"], notes=row["notes"], rating=row["rating"],
        isbn=row["isbn"], cover_url=row["cover_url"],
        spine_path=row["spine_path"], cover_path=row["cover_path"],
    )


def init_db() -> None:
    with closing(_connect()) as conn, conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT 'Запланировано',
                notes TEXT NOT NULL DEFAULT '',
                rating INTEGER NOT NULL DEFAULT 0,
                isbn TEXT NOT NULL DEFAULT '',
                cover_url TEXT NOT NULL DEFAULT '',
                spine_path TEXT NOT NULL DEFAULT '',
                cover_path TEXT NOT NULL DEFAULT ''
            )
        """)
        # база, созданная раньше, не имеет колонки cover_path: добавляем
        columns = {r["name"] for r in conn.execute("PRAGMA table_info(books)")}
        if "cover_path" not in columns:
            conn.execute("ALTER TABLE books ADD COLUMN cover_path TEXT NOT NULL DEFAULT ''")


def get_books() -> list[Book]:
    with closing(_connect()) as conn:
        rows = conn.execute("SELECT * FROM books ORDER BY id DESC").fetchall()
    return [_to_book(r) for r in rows]


def get_book(book_id: int) -> Book | None:
    with closing(_connect()) as conn:
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    return _to_book(row) if row else None


def save_book(book: Book) -> Book:
    values = (book.title, book.author, book.status, book.notes, book.rating,
              book.isbn, book.cover_url, book.spine_path, book.cover_path)
    with closing(_connect()) as conn, conn:
        if book.id is None:
            cur = conn.execute(
                "INSERT INTO books (title, author, status, notes, rating, isbn, "
                "cover_url, spine_path, cover_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                values)
            book.id = cur.lastrowid
        else:
            conn.execute(
                "UPDATE books SET title=?, author=?, status=?, notes=?, rating=?, "
                "isbn=?, cover_url=?, spine_path=?, cover_path=? WHERE id=?",
                (*values, book.id))
    return book


def delete_book(book: Book) -> None:
    if book.id is None:
        return
    for path in (book.spine_path, book.cover_path):
        if path:
            Path(path).unlink(missing_ok=True)
    with closing(_connect()) as conn, conn:
        conn.execute("DELETE FROM books WHERE id = ?", (book.id,))