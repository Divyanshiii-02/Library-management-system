"""Load circulation records into Pandas and create simple analytics charts."""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from .database import connect

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "charts"


def load_transactions():
    with connect() as db:
        return pd.read_sql_query("""SELECT t.id, b.title, b.category, m.name AS member,
            t.issue_date, t.due_date, t.return_date, t.fine
            FROM transactions t JOIN books b ON b.id=t.book_id
            JOIN members m ON m.id=t.member_id""", db, parse_dates=["issue_date", "due_date", "return_date"])


def create_charts(show=False):
    data = load_transactions()
    OUTPUT_DIR.mkdir(exist_ok=True)
    if data.empty:
        return []
    files = []
    charts = [
        (data["title"].value_counts().head(10), "Most Borrowed Books", "Book", "Borrow count", "most_borrowed_books.png"),
        (data.assign(day=data["issue_date"].dt.day_name())["day"].value_counts().reindex(
            ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"], fill_value=0),
         "Borrowing by Day of Week", "Day", "Borrow count", "peak_borrowing_days.png"),
        (data["category"].value_counts(), "Category-wise Usage", "Category", "Borrow count", "category_usage.png"),
    ]
    for series, title, xlabel, ylabel, filename in charts:
        fig, ax = plt.subplots(figsize=(9, 5))
        series.plot(kind="bar", ax=ax, color="#3569a8")
        ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
        fig.tight_layout()
        path = OUTPUT_DIR / filename
        fig.savefig(path, dpi=150)
        files.append(path)
        if show:
            plt.show()
        plt.close(fig)
    return files
