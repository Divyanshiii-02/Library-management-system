# Library Management System with Analytics

A menu-driven Python project using object-oriented domain models, SQLite, Pandas, and Matplotlib. It supports book and member registration, searching, book loans and returns, automatic overdue fines, and usage charts.

## Requirements

- Python 3.10 or later
- `pip`

## Setup and run

Open a terminal in this project folder and run:

```bash
python -m venv .venv
```

Activate the environment:

- Windows PowerShell: `.venv\Scripts\Activate.ps1`
- Windows Command Prompt: `.venv\Scripts\activate.bat`
- macOS/Linux: `source .venv/bin/activate`

Install packages and start the application:

```bash
python -m pip install -r requirements.txt
python main.py
```

The program creates `library.db` automatically the first time it runs. Data stays in that SQLite file. Analytics charts are saved under `charts/`.

## Suggested first use

1. Choose **1** and add books with their category and copy count.
2. Choose **2** to register members. Email addresses must be unique.
3. Use **3** to search or list books.
4. Choose **4** to issue a book. The loan period is 14 days.
5. Choose **5** to return a book. The default fine is ₹2 per overdue day; change `FINE_PER_DAY` in `library_app/service.py` if your assignment specifies another rate.
6. Choose **7** to view Pandas summaries or **8** to save three chart images.

## Project layout

```text
library_management_project/
├── main.py
├── requirements.txt
├── README.md
└── library_app/
    ├── __init__.py
    ├── analytics.py
    ├── cli.py
    ├── database.py
    ├── models.py
    └── service.py
```

`Book`, `Member`, and `Transaction` are model classes. `service.py` implements database-backed operations; `database.py` creates the schema; `analytics.py` loads transaction rows into a Pandas DataFrame and generates visualizations; `cli.py` provides the menu.
