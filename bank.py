import os
from datetime import datetime

# Store all user accounts in memory
accounts = {}
next_account_number = 100001  # Start sequential account numbers
login_username = "admin"
login_password = "7777"

# Save all accounts to a single file
def save_all_accounts():
    with open("accounts.txt", "w") as file:
        for acc_no, details in accounts.items():
            file.write(f"{acc_no}|{details['name']}|{details['address']}|{details['phone']}|{details['password']}|{details['balance']}\n")

# Log transaction to a single file
def log_transaction(acc_no, txn_type, amount):
    date_str = datetime.now().strftime('%Y-%m-%d')
    with open("transactions.txt", "a") as txn:
        txn.write(f"{date_str} | {acc_no} | {txn_type} | {amount}\n")

# Generate account number
def generate_account_number():
    global next_account_number
    acc_no = str(next_account_number)
    next_account_number += 1
    return acc_no

# Verify account password
def verify_password(acc_no):
    input_pwd = input("Enter account password: ")
    return input_pwd == accounts[acc_no]['password']

# Create a new account
def create_account():
    name = input("Enter account holder name: ")
    address = input("Enter address: ")
    phone = input("Enter phone number: ")
    password = input("Set a password for the account: ")
    acc_no = generate_account_number()
    try:
        balance = float(input("Enter initial balance: "))
        if balance < 0:
            print("Error: Initial balance must be non-negative.")
            return
    except ValueError:
        print("Error: Invalid amount.")
        return

#Store the new account data 
    accounts[acc_no] = {
        'name': name,
        'address': address,
        'phone': phone,
        'password': password,
        'balance': balance,
        'transactions': [{
            'date': datetime.now().strftime("%Y-%m-%d"),
            'type': "Created Account",
            'amount': balance
        }]
    }

    save_all_accounts()
    log_transaction(acc_no, "Created Account", balance)
    print(f"Account created successfully! Your account number is: {acc_no}")

# Deposit money
def deposit_money():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Error: Account not found.")
        return
    if not verify_password(acc_no):
        print("Error: Incorrect password.")
        return

    try:
        amount = float(input("Enter amount to deposit: "))
        if amount <= 0:
            print("Error: Must deposit a positive amount.")
            return
    except ValueError:
        print("Error: Invalid amount.")
        return

    accounts[acc_no]['balance'] += amount
    txn_data = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'type': "Deposit",
        'amount': amount
    }
    accounts[acc_no]['transactions'].append(txn_data)

    log_transaction(acc_no, "Deposit", amount)
    save_all_accounts()
    print("Deposit successful.")

# Withdraw money
def withdraw_money():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Error: Account not found.")
        return
    if not verify_password(acc_no):
        print("Error: Incorrect password.")
        return

    try:
        amount = float(input("Enter amount to withdraw: "))
        if amount <= 0 or amount > accounts[acc_no]['balance']:
            print("Error: Invalid withdrawal amount.")
            return
    except ValueError:
        print("Error: Invalid amount.")
        return

    accounts[acc_no]['balance'] -= amount
    txn_data = {
        'date': datetime.now().strftime("%Y-%m-%d"),
        'type': "Withdrawal",
        'amount': amount
    }
    accounts[acc_no]['transactions'].append(txn_data)

    log_transaction(acc_no, "Withdrawal", amount)
    save_all_accounts()
    print("Withdrawal successful.")

# Check balance
def check_balance():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        if not verify_password(acc_no):
            print("Error: Incorrect password.")
            return
        print(f"Account Balance: {accounts[acc_no]['balance']}")
    else:
        print("Error: Account not found.")

# Show transaction history
def show_transaction_history():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Error: Account not found.")
        return
    if not verify_password(acc_no):
        print("Error: Incorrect password.")
        return

    print("\n--- Transaction History ---")
    print("{:<12} {:<15} {:<10}".format("Date", "Type", "Amount"))
    print("-" * 40)
    for txn in accounts[acc_no]['transactions']:
        print("{:<12} {:<15} {:<10}".format(txn['date'], txn['type'], txn['amount']))
    print("-" * 40)

# Admin login
def login():
    print("=== Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    if username == login_username and password == login_password:
        print("Login successful!\n")
        return True
    else:
        print("Invalid login. Exiting...")
        return False

# Main menu
def menu():
    while True:
        print("\n--- Mini Banking App ---")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")
        if choice == '1':
            create_account()
        elif choice == '2':
            deposit_money()
        elif choice == '3':
            withdraw_money()
        elif choice == '4':
            check_balance()
        elif choice == '5':
            show_transaction_history()
        elif choice == '6':
            print("Thank you for using the banking app!")
            break
        else:
            print("Invalid choice. Please try again.")

# Start the app
if login():
    menu()


































                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            
            

