"""Business operations for books, members, borrowing, and returns."""
from datetime import date, timedelta
from .database import connect
from .models import Book, Member, Transaction

LOAN_DAYS = 14
FINE_PER_DAY = 2.0  # Change this value to set the library's daily late fee.


def add_book(title, author, category, copies):
    if copies < 1:
        raise ValueError("Number of copies must be at least 1.")
    with connect() as db:
        db.execute("INSERT INTO books(title, author, category, total_copies, available_copies) VALUES (?, ?, ?, ?, ?)",
                   (title.strip(), author.strip(), category.strip(), copies, copies))


def add_member(name, email, phone=""):
    with connect() as db:
        db.execute("INSERT INTO members(name, email, phone) VALUES (?, ?, ?)",
                   (name.strip(), email.strip().lower(), phone.strip()))


def search_books(term=""):
    pattern = f"%{term.strip()}%"
    with connect() as db:
        rows = db.execute("SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR category LIKE ? ORDER BY id",
                          (pattern, pattern, pattern)).fetchall()
    return [Book(**dict(row)) for row in rows]


def list_members():
    with connect() as db:
        rows = db.execute("SELECT * FROM members ORDER BY id").fetchall()
    return [Member(**dict(row)) for row in rows]


def issue_book(book_id, member_id):
    today = date.today()
    due = today + timedelta(days=LOAN_DAYS)
    with connect() as db:
        book = db.execute("SELECT available_copies FROM books WHERE id=?", (book_id,)).fetchone()
        if not book:
            raise ValueError("Book ID not found.")
        if book["available_copies"] < 1:
            raise ValueError("No copies are currently available.")
        if not db.execute("SELECT id FROM members WHERE id=?", (member_id,)).fetchone():
            raise ValueError("Member ID not found.")
        db.execute("UPDATE books SET available_copies=available_copies-1 WHERE id=?", (book_id,))
        db.execute("INSERT INTO transactions(book_id, member_id, issue_date, due_date) VALUES (?, ?, ?, ?)",
                   (book_id, member_id, today.isoformat(), due.isoformat()))
    return due


def return_book(transaction_id):
    today = date.today()
    with connect() as db:
        txn = db.execute("SELECT * FROM transactions WHERE id=?", (transaction_id,)).fetchone()
        if not txn:
            raise ValueError("Transaction ID not found.")
        if txn["return_date"]:
            raise ValueError("This book has already been returned.")
        due = date.fromisoformat(txn["due_date"])
        fine = max(0, (today - due).days) * FINE_PER_DAY
        db.execute("UPDATE transactions SET return_date=?, fine=? WHERE id=?",
                   (today.isoformat(), fine, transaction_id))
        db.execute("UPDATE books SET available_copies=available_copies+1 WHERE id=?", (txn["book_id"],))
    return fine


def active_transactions():
    with connect() as db:
        return db.execute("""SELECT t.id, b.title, m.name, t.issue_date, t.due_date
            FROM transactions t JOIN books b ON b.id=t.book_id JOIN members m ON m.id=t.member_id
            WHERE t.return_date IS NULL ORDER BY t.due_date""").fetchall()
