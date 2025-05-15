import os # For the file existence check
from datetime import datetime # For handling current date/time

# Global storage for accounts
accounts = {} #Dictionary to store account details
next_account_number = 100001 #Starting point of new account numbers


# Returns the current date in YYYY-MM-DD format
def current_date():
    return datetime.now().strftime('%Y-%m-%d')

# Checks if a given value is a positive float
def is_positive_float(value):
    try:
        val = float(value)
        return val > 0
    except ValueError:
        return False

# Load accounts and transactions from files if they exist
def load_accounts():
    global next_account_number
    if os.path.exists("accounts.txt"):
        try:
            with open("accounts.txt", "r") as file:
                for line in file:
                    acc_no, name, address, phone, password, balance = line.strip().split("|")
                    accounts[acc_no] = {
                        'name': name,
                        'address': address,
                        'phone': phone,
                        'password': password,
                        'balance': float(balance),
                        'transactions': []
                    }
                # Update next available account number
                next_account_number = max(int(acc) for acc in accounts.keys()) + 1
        except Exception as e:
            print("Error loading accounts data:", e)

    # Load transaction history
    if os.path.exists("transactions.txt"):
        try:
            with open("transactions.txt", "r") as txn_file:
                for line in txn_file:
                    parts = line.strip().split(" | ")
                    if len(parts) == 4:
                        date, acc_no, txn_type, amount = parts
                        if acc_no in accounts:
                            accounts[acc_no]['transactions'].append({
                                'date': date,
                                'type': txn_type,
                                'amount': float(amount)
                            })
        except Exception as e:
            print("Error loading transactions:", e)

# Save all account data to file
def save_all_accounts():
    try:
        with open("accounts.txt", "w") as file:
            for acc_no, details in accounts.items():
                file.write(f"{acc_no}|{details['name']}|{details['address']}|{details['phone']}|{details['password']}|{details['balance']}\n")
    except IOError as e:
        print("Failed to save account data:", e)

# Log a transaction to the file
def log_transaction(acc_no, txn_type, amount):
    try:
        with open("transactions.txt", "a") as txn:
            txn.write(f"{current_date()} | {acc_no} | {txn_type} | {amount}\n")
    except IOError as e:
        print("Failed to log transaction:", e)

# Create a new account
def create_account():
    global next_account_number
    name = input("Enter account holder name: ")
    address = input("Enter address: ")
    phone = input("Enter phone number: ")
    password = input("Set a password: ")
    initial = input("Enter initial balance: ")

    if not is_positive_float(initial):
        print("Invalid balance. Please enter a positive number.")
        return

    balance = float(initial)
    acc_no = str(next_account_number)
    next_account_number += 1

    accounts[acc_no] = {
        'name': name,
        'address': address,
        'phone': phone,
        'password': password,
        'balance': balance,
        'transactions': [{
            'date': current_date(),
            'type': "Created Account",
            'amount': balance
        }]
    }

    save_all_accounts()
    log_transaction(acc_no, "Created Account", balance)
    print(f"Account created successfully! Your account number is: {acc_no}")

# Customer login
def customer_login():
    acc_no = input("Enter your account number: ")
    password = input("Enter your password: ")
    if acc_no in accounts and accounts[acc_no]['password'] == password:
        print(f"\nWelcome, {accounts[acc_no]['name']}!")
        return acc_no
    else:
        print("Login failed: Invalid credentials.")
        return None

# Deposit money
def deposit_money(acc_no):
    amount_input = input("Enter amount to deposit: ")
    if not is_positive_float(amount_input):
        print("Amount must be a positive number.")
        return

    amount = float(amount_input)
    accounts[acc_no]['balance'] += amount
    accounts[acc_no]['transactions'].append({
        'date': current_date(),
        'type': "Deposit",
        'amount': amount
    })
    log_transaction(acc_no, "Deposit", amount)
    save_all_accounts()
    print("Deposit successful.")

# Withdraw money
def withdraw_money(acc_no):
    amount_input = input("Enter amount to withdraw: ")
    if not is_positive_float(amount_input):
        print("Amount must be a positive number.")
        return

    amount = float(amount_input)
    if amount > accounts[acc_no]['balance']:
        print("Insufficient funds.")
        return

    accounts[acc_no]['balance'] -= amount
    accounts[acc_no]['transactions'].append({
        'date': current_date(),
        'type': "Withdrawal",
        'amount': amount
    })
    log_transaction(acc_no, "Withdrawal", amount)
    save_all_accounts()
    print("Withdrawal successful.")

# Check account balance
def check_balance(acc_no):
    print(f"Your current balance is: {accounts[acc_no]['balance']}")

# Show transaction history
def show_transaction_history(acc_no):
    print("\n--- Transaction History ---")
    print("{:<12} {:<20} {:<10}".format("Date", "Type", "Amount"))
    print("-" * 45)
    for txn in accounts[acc_no]['transactions']:
        print("{:<12} {:<20} {:<10}".format(txn['date'], txn['type'], txn['amount']))
    print("-" * 45)

# Customer menu
def customer_menu(acc_no):
    while True:
        print("\n--- Banking Menu ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Logout")

        choice = input("Enter your choice: ")
        if choice == '1':
            deposit_money(acc_no)
        elif choice == '2':
            withdraw_money(acc_no)
        elif choice == '3':
            check_balance(acc_no)
        elif choice == '4':
            show_transaction_history(acc_no)
        elif choice == '5':
            print("Logged out.")
            break
        else:
            print("Invalid choice.")

# Start the app
def start_app():
    load_accounts()
    print("=== Welcome to Mini Banking App ===")

    while True:
        print("\n1. Create New Account")
        print("2. Login as Customer")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            acc_no = customer_login()
            if acc_no:
                customer_menu(acc_no)
        elif choice == '3':
            print("Thank you for using this app. Goodbye!")
            break
        else:
            print("Invalid option.")

# Run the application
start_app()


