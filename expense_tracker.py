import csv
import json
import os
from datetime import datetime

DATA_FILE = "expenses.csv"
CATEGORIES = ["Food", "Transport", "Shopping", "Entertainment", "Health", "Education", "Other"]

def initialize_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "date", "category", "description", "amount"])
            writer.writeheader()

def load_expenses():
    expenses = []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["amount"] = float(row["amount"])
            expenses.append(row)
    return expenses

def save_expenses(expenses):
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "date", "category", "description", "amount"])
        writer.writeheader()
        writer.writerows(expenses)

def generate_id(expenses):
    if not expenses:
        return "1"
    return str(max(int(e["id"]) for e in expenses) + 1)

def add_expense():
    print("\n--- Add Expense ---")
    print("Categories:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    
    while True:
        try:
            choice = int(input("Select category (1-7): "))
            if 1 <= choice <= 7:
                category = CATEGORIES[choice - 1]
                break
            print("Enter a number between 1 and 7.")
        except ValueError:
            print("Invalid input.")

    description = input("Description: ").strip()
    if not description:
        description = "N/A"

    while True:
        try:
            amount = float(input("Amount (Rs): "))
            if amount <= 0:
                print("Amount must be positive.")
                continue
            break
        except ValueError:
            print("Enter a valid number.")

    date_input = input("Date (DD-MM-YYYY) or press Enter for today: ").strip()
    if not date_input:
        date = datetime.now().strftime("%d-%m-%Y")
    else:
        try:
            datetime.strptime(date_input, "%d-%m-%Y")
            date = date_input
        except ValueError:
            print("Invalid date. Using today.")
            date = datetime.now().strftime("%d-%m-%Y")

    expenses = load_expenses()
    expense = {
        "id": generate_id(expenses),
        "date": date,
        "category": category,
        "description": description,
        "amount": amount
    }
    expenses.append(expense)
    save_expenses(expenses)
    print(f"\nAdded: Rs {amount:.2f} for {category} — {description} on {date}")

def view_expenses():
    print("\n--- All Expenses ---")
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    print(f"\n{'ID':<5} {'Date':<12} {'Category':<15} {'Description':<20} {'Amount':>10}")
    print("-" * 65)
    total = 0
    for e in expenses:
        desc = e['description'][:18] + ".." if len(e['description']) > 18 else e['description']
        print(f"{e['id']:<5} {e['date']:<12} {e['category']:<15} {desc:<20} Rs {e['amount']:>8.2f}")
        total += e["amount"]
    print("-" * 65)
    print(f"{'TOTAL':<53} Rs {total:>8.2f}")

def delete_expense():
    print("\n--- Delete Expense ---")
    view_expenses()
    expenses = load_expenses()
    if not expenses:
        return

    expense_id = input("\nEnter ID to delete (or 0 to cancel): ").strip()
    if expense_id == "0":
        return

    original_count = len(expenses)
    expenses = [e for e in expenses if e["id"] != expense_id]

    if len(expenses) == original_count:
        print(f"No expense found with ID {expense_id}.")
    else:
        save_expenses(expenses)
        print(f"Deleted expense ID {expense_id}.")

def monthly_summary():
    print("\n--- Monthly Summary ---")
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return

    months = {}
    for e in expenses:
        month_key = e["date"][3:]  # MM-YYYY
        months.setdefault(month_key, {"total": 0, "categories": {}})
        months[month_key]["total"] += e["amount"]
        cat = e["category"]
        months[month_key]["categories"][cat] = months[month_key]["categories"].get(cat, 0) + e["amount"]

    for month, data in sorted(months.items()):
        print(f"\n  {month}")
        print(f"  {'Category':<20} {'Amount':>10}")
        print("  " + "-" * 32)
        for cat, amt in sorted(data["categories"].items(), key=lambda x: -x[1]):
            print(f"  {cat:<20} Rs {amt:>8.2f}")
        print("  " + "-" * 32)
        print(f"  {'TOTAL':<20} Rs {data['total']:>8.2f}")

def export_json():
    expenses = load_expenses()
    if not expenses:
        print("No expenses to export.")
        return
    filename = f"expenses_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=2)
    print(f"Exported {len(expenses)} expenses to {filename}")

def search_by_category():
    print("\n--- Search by Category ---")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    try:
        choice = int(input("Select category (1-7): "))
        if not 1 <= choice <= 7:
            print("Invalid choice.")
            return
    except ValueError:
        print("Invalid input.")
        return

    category = CATEGORIES[choice - 1]
    expenses = load_expenses()
    filtered = [e for e in expenses if e["category"] == category]

    if not filtered:
        print(f"No expenses found for {category}.")
        return

    total = sum(e["amount"] for e in filtered)
    print(f"\n{category} expenses:")
    print(f"{'ID':<5} {'Date':<12} {'Description':<22} {'Amount':>10}")
    print("-" * 52)
    for e in filtered:
        desc = e['description'][:20] + ".." if len(e['description']) > 20 else e['description']
        print(f"{e['id']:<5} {e['date']:<12} {desc:<22} Rs {e['amount']:>8.2f}")
    print("-" * 52)
    print(f"{'Total':<40} Rs {total:>8.2f}")

def main():
    initialize_file()
    print("=" * 45)
    print("     EXPENSE TRACKER — Personal Finance")
    print("=" * 45)

    while True:
        print("\n  1. Add expense")
        print("  2. View all expenses")
        print("  3. Delete expense")
        print("  4. Monthly summary")
        print("  5. Search by category")
        print("  6. Export to JSON")
        print("  0. Exit")

        choice = input("\nChoice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            delete_expense()
        elif choice == "4":
            monthly_summary()
        elif choice == "5":
            search_by_category()
        elif choice == "6":
            export_json()
        elif choice == "0":
            print("\nGoodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
