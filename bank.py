import os
from datetime import datetime

# Global storage for accounts and next account number
accounts = {}
login_username = "admin"
login_password = "7777"
next_account_number = 100001  # Start account numbers from here

# Load existing account data from file
def load_accounts():
    global next_account_number
    if os.path.exists("accounts.txt"):
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
        next_account_number = max(int(acc) for acc in accounts.keys()) + 1

# Save all account data to file
def save_all_accounts():
    with open("accounts.txt", "w") as file:
        for acc_no, details in accounts.items():
            file.write(f"{acc_no}|{details['name']}|{details['address']}|{details['phone']}|{details['password']}|{details['balance']}\n")

# Save each transaction to file
def log_transaction(acc_no, txn_type, amount):
    date_str = datetime.now().strftime('%Y-%m-%d')
    with open("transactions.txt", "a") as txn:
        txn.write(f"{date_str} | {acc_no} | {txn_type} | {amount}\n")

# Admin creates a new account
def create_account():
    global next_account_number
    name = input("Enter account holder name: ")
    address = input("Enter address: ")
    phone = input("Enter phone number: ")
    password = input("Set a password (not used for login): ")

    try:
        balance = float(input("Enter initial balance: "))
        if balance < 0:
            print("Error: Balance cannot be negative.")
            return
    except ValueError:
        print("Invalid balance.")
        return

    acc_no = str(next_account_number)
    next_account_number += 1

    accounts[acc_no] = {
        'name': name,
        'address': address,
        'phone': phone,
        'password': password,
        'balance': balance,
        'transactions': [{
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': "Created Account",
            'amount': balance
        }]
    }

    save_all_accounts()
    log_transaction(acc_no, "Created Account", balance)
    print(f"Account created successfully! Your account number is: {acc_no}")

# Customer login using name and address
def customer_login():
    name = input("Enter your name: ")
    address = input("Enter your address: ")
    for acc_no, info in accounts.items():
        if info['name'] == name and info['address'] == address:
            print(f"\nWelcome, {info['name']}!")
            return acc_no
    print("Login failed: No matching account found.")
    return None

# Deposit money
def deposit_money(acc_no):
    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Must deposit positive amount.")
            return
        accounts[acc_no]['balance'] += amount
        accounts[acc_no]['transactions'].append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': "Deposit",
            'amount': amount
        })
        log_transaction(acc_no, "Deposit", amount)
        save_all_accounts()
        print("Deposit successful.")
    except ValueError:
        print("Invalid amount.")

# Withdraw money
def withdraw_money(acc_no):
    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0 or amount > accounts[acc_no]['balance']:
            print("Invalid withdrawal amount.")
            return
        accounts[acc_no]['balance'] -= amount
        accounts[acc_no]['transactions'].append({
            'date': datetime.now().strftime('%Y-%m-%d'),
            'type': "Withdrawal",
            'amount': amount
        })
        log_transaction(acc_no, "Withdrawal", amount)
        save_all_accounts()
        print("Withdrawal successful.")
    except ValueError:
        print("Invalid amount.")

# Check balance
def check_balance(acc_no):
    print(f"Your current balance is: {accounts[acc_no]['balance']}")

# Show transaction history
def show_transaction_history(acc_no):
    print("\n--- Transaction History ---")
    print("{:<12} {:<15} {:<10}".format("Date", "Type", "Amount"))
    print("-" * 40)
    for txn in accounts[acc_no]['transactions']:
        print("{:<12} {:<15} {:<10}".format(txn['date'], txn['type'], txn['amount']))
    print("-" * 40)

# Transfer money between accounts
def transfer_money(sender_acc):
    receiver_acc = input("Enter recipient account number: ")
    if receiver_acc not in accounts:
        print("Recipient account not found.")
        return
    if receiver_acc == sender_acc:
        print("You cannot transfer to the same account.")
        return

    try:
        amount = float(input("Enter amount to transfer: "))
        if amount <= 0:
            print("Amount must be positive.")
            return
        if amount > accounts[sender_acc]['balance']:
            print("Insufficient balance.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    # Deduct from sender
    accounts[sender_acc]['balance'] -= amount
    accounts[sender_acc]['transactions'].append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': f"Transfer to {receiver_acc}",
        'amount': amount
    })

    # Add to receiver
    accounts[receiver_acc]['balance'] += amount
    accounts[receiver_acc]['transactions'].append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'type': f"Received from {sender_acc}",
        'amount': amount
    })

    # Log both
    log_transaction(sender_acc, f"Transfer to {receiver_acc}", amount)
    log_transaction(receiver_acc, f"Received from {sender_acc}", amount)
    save_all_accounts()
    print("Transfer successful.")

# Customer menu
def customer_menu(acc_no):
    while True:
        print("\n--- Banking Menu ---")
        print("1. Deposit Money")
        print("2. Withdraw Money")
        print("3. Check Balance")
        print("4. Transaction History")
        print("5. Transfer Money")
        print("6. Logout")

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
            transfer_money(acc_no)
        elif choice == '6':
            print("Logged out.")
            break
        else:
            print("Invalid choice.")

# Admin login
def admin_login():
    print("=== Admin Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    return username == login_username and password == login_password

# Start the application
def start_app():
    load_accounts()
    print("=== Welcome to Mini Banking App ===")

    print("\n--- Admin Login Required to Start App ---")
    if not admin_login():
        print("Admin login failed. Exiting app.")
        return
    print("Admin login successful!")

    while True:
        print("\n1. Create New Account")
        print("2. Login as Customer (by Name & Address)")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            create_account()
        elif choice == '2':
            acc_no = customer_login()
            if acc_no:
                customer_menu(acc_no)
        elif choice == '3':
            print("thank you for using this app. Goodbye!")
            break
        else:
            print("Invalid option.")

# Run the app
start_app()
































                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            
            

