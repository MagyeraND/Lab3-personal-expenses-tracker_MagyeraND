import os
import time

def read_balance():
    if not os.path.isfile("balance.txt"):
        f = open("balance.txt", "w")
        f.write("0")
        f.close()
        return 0
    f = open("balance.txt", "r")
    data = f.read().strip()
    f.close()
    try:
        return float(data)
    except:
        return 0

def write_balance(amount):
    f = open("balance.txt", "w")
    f.write(str(amount))
    f.close()

def show_menu():
    print("\n=== EXPENSE TRACKER ===")
    print("1. Check Balance")
    print("2. View Expenses")
    print("3. Add Expense")
    print("4. Archive Expense File")
    print("5. Exit")
    print("======================")

def check_balance():
    bal = read_balance()
    total = 0
    for file in os.listdir("."):
        if file.startswith("expenses_") and file.endswith(".txt"):
            f = open(file, "r")
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    try:
                        total += float(parts[2])
                    except:
                        pass
            f.close()
    available = bal - total
    print("\nStored Balance:", bal)
    print("Total Expenses:", total)
    print("Available:", available)
    ans = input("Add money? (y/n): ").lower().strip()
    if ans == "y":
        amt = input("Amount to add: ").strip()
        try:
            amt = float(amt)
            if amt > 0:
                write_balance(bal + amt)
                print("Balance updated! New balance:", bal + amt)
            else:
                print("Amount must be positive!")
        except:
            print("Invalid amount!")

def add_expense():
    bal = read_balance()
    print("\nAvailable Balance:", bal)
    date = input("Enter date (YYYY-MM-DD): ").strip()
    filename = "expenses_" + date + ".txt"
    item = input("Item name: ").strip()
    amt = input("Amount spent: ").strip()
    try:
        amt = float(amt)
    except:
        print("Invalid amount!")
        return
    print("\nYou entered:")
    print("Date:", date)
    print("Item:", item)
    print("Amount:", amt)
    confirm = input("Confirm? (y/n): ").lower().strip()
    if confirm != "y":
        print("Cancelled.")
        return
    if amt > bal:
        print("Insufficient balance!")
        return
    expense_id = 1
    if os.path.isfile(filename):
        f = open(filename, "r")
        lines = f.readlines()
        f.close()
        expense_id = len(lines) + 1
    now = time.asctime()
    f = open(filename, "a")
    f.write(str(expense_id) + "|" + item + "|" + str(amt) + "|" + now + "\n")
    f.close()
    write_balance(bal - amt)
    print("Expense saved! Remaining balance:", bal - amt)

def search_expenses(value, mode):
    found = False
    for file in os.listdir("."):
        if file.startswith("expenses_"):
            f = open(file, "r")
            lines = f.readlines()
            f.close()
            for ln in lines:
                parts = ln.strip().split("|")
                if len(parts) == 4:
                    item = parts[1].lower()
                    amt = float(parts[2])
                    if mode == "name" and value in item:
                        print(file, "-", ln.strip())
                        found = True
                    elif mode == "amount" and amt == value:
                        print(file, "-", ln.strip())
                        found = True
    if not found:
        print("No results found.")

def view_expenses():
    print("\n1. Search by item")
    print("2. Search by amount")
    print("3. Back")
    choice = input("Choose: ").strip()
    if choice == "1":
        term = input("Item name to search: ").lower().strip()
        search_expenses(term, "name")
    elif choice == "2":
        amt = input("Amount to search: ").strip()
        try:
            amt = float(amt)
            search_expenses(amt, "amount")
        except:
            print("Invalid amount!")
    else:
        return

def archive_file():
    date = input("Enter date (YYYY-MM-DD) to archive: ").strip()
    filename = "expenses_" + date + ".txt"
    if not os.path.isfile(filename):
        print("No file found for that date.")
        return
    if not os.path.isdir("archives"):
        os.mkdir("archives")
    new_path = "archives/" + filename
    os.rename(filename, new_path)
    f = open("archive_log.txt", "a")
    f.write("Archived " + filename + " at " + time.asctime() + "\n")
    f.close()
    print("File archived!")

while True:
    show_menu()
    choice = input("Select: ").strip()
    if choice == "1":
        check_balance()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        add_expense()
    elif choice == "4":
        archive_file()
    elif choice == "5":
        print("Exiting...")
        break
    else:
        print("Invalid choice!")
