"""Interactive command-line menu."""
from .database import initialize_database, connect
from .service import add_book, add_member, search_books, list_members, issue_book, return_book, active_transactions
from .analytics import load_transactions, create_charts


def show_books(books):
    if not books:
        print("No books found.")
        return
    print("\nID | Title | Author | Category | Available/Total")
    for b in books:
        print(f"{b.id} | {b.title} | {b.author} | {b.category} | {b.available_copies}/{b.total_copies}")


def menu():
    initialize_database()
    actions = {
        "1": "Add book", "2": "Add member", "3": "Search/list books",
        "4": "Issue book", "5": "Return book", "6": "Show active loans",
        "7": "Show transaction analysis", "8": "Create analytics charts", "0": "Exit"
    }
    while True:
        print("\n=== Library Management System ===")
        for key, label in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose: ").strip()
        try:
            if choice == "1":
                title = input("Title: "); author = input("Author: "); category = input("Category: ")
                copies = int(input("Number of copies: "))
                add_book(title, author, category, copies)
                print("Book added.")
            elif choice == "2":
                name = input("Member name: "); email = input("Email: "); phone = input("Phone (optional): ")
                add_member(name, email, phone)
                print("Member added.")
            elif choice == "3":
                show_books(search_books(input("Search title/author/category (blank for all): ")))
            elif choice == "4":
                show_books(search_books())
                member_ids = [m.id for m in list_members()]
                print("Members:", ", ".join(f"{m.id}: {m.name}" for m in list_members()) or "none")
                due = issue_book(int(input("Book ID: ")), int(input("Member ID: ")))
                print(f"Book issued. Due date: {due}")
            elif choice == "5":
                print("Active loans (ID | Book | Member | Issue | Due)")
                for row in active_transactions():
                    print(" | ".join(str(value) for value in row))
                fine = return_book(int(input("Transaction ID to return: ")))
                print(f"Book returned. Late fine: ₹{fine:.2f}")
            elif choice == "6":
                for row in active_transactions(): print(" | ".join(str(value) for value in row))
            elif choice == "7":
                data = load_transactions()
                if data.empty: print("No transactions yet.")
                else:
                    print("\nBorrow count by book:\n", data["title"].value_counts().to_string())
                    print("\nBorrow count by category:\n", data["category"].value_counts().to_string())
                    print("\nBorrow count by weekday:\n", data["issue_date"].dt.day_name().value_counts().to_string())
            elif choice == "8":
                files = create_charts()
                print("No transaction data yet." if not files else "Charts saved:\n" + "\n".join(map(str, files)))
            elif choice == "0":
                print("Goodbye!"); break
            else:
                print("Please choose a listed option.")
        except (ValueError, TypeError) as error:
            print(f"Could not complete the request: {error}")
        except Exception as error:
            # Includes database constraints such as duplicate member email.
            print(f"Could not complete the request: {error}")
