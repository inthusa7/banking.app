import os   # For the file existence check
from datetime import datetime  # For handling current date/time

# Global storage for accounts and admin credentials
accounts = {}     #Dictionary to store account details
login_username = ""  #admin username
login_password = ""   #admin userpassword
next_account_number = 100001 #Starting point of new account numbers

# Function to returns the current date in YYYY-MM-DD format
def current_date():
    return datetime.now().strftime('%Y-%m-%d')

# Function to Checks if a given value is a positive float
def is_positive_float(value):
    try:
        val = float(value)
        return val > 0
    except ValueError:
        return False

# Load existing accounts and transactions data from files 
def load_accounts():
    global next_account_number 
    # Check and load account data 
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
                        'transactions': []  #Emty list to store transaction
                    }
                # Set next account number to be higher than the highest existing one
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

# Save all account information back to the  file
def save_all_accounts():
    try:
        with open("accounts.txt", "w") as file:
            for acc_no, details in accounts.items():
                file.write(f"{acc_no}|{details['name']}|{details['address']}|{details['phone']}|{details['password']}|{details['balance']}\n")
    except IOError as e:
        print("Failed to save account data:", e)

# Append a single transaction to the transaction log file
def log_transaction(acc_no, txn_type, amount):
    try:
        with open("transactions.txt", "a") as txn:
            txn.write(f"{current_date()} | {acc_no} | {txn_type} | {amount}\n")
    except IOError as e:
        print("Failed to log transaction:", e)

# Create a new account with user input
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
    next_account_number += 1  #Update for next account 

    #Store account info in dictionary
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
    
    #Save to file and log creation
    save_all_accounts()
    log_transaction(acc_no, "Created Account", balance)
    print(f"Account created successfully! Your account number is: {acc_no}")

#login using account number and password
def customer_login():
    acc_no = input("Enter your account number: ")
    password = input("Enter your password: ")
    if acc_no in accounts and accounts[acc_no]['password'] == password:
        print(f"\nWelcome, {accounts[acc_no]['name']}!")
        return acc_no
    else:
        print("Login failed: Invalid credentials.")
        return None

# Add money to an account
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

# Withdraw money if balance allows
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

# Display current balance
def check_balance(acc_no):
    print(f"Your current balance is: {accounts[acc_no]['balance']}")

# Show list of transaction 
def show_transaction_history(acc_no):
    print("\n--- Transaction History ---")
    print("{:<12} {:<20} {:<10}".format("Date", "Type", "Amount"))
    print("-" * 45)
    for txn in accounts[acc_no]['transactions']:
        print("{:<12} {:<20} {:<10}".format(txn['date'], txn['type'], txn['amount']))
    print("-" * 45)



# Display option for the logged-in customer
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

# Admin setup or login (only first time)
def admin_setup_or_login():
    global login_username, login_password

    # Skip login if already verified
    if os.path.exists("admin.txt"):
        return True

    # First-time setup
    if not os.path.exists("admin.txt"):
        print("=== First Time Setup: Create Admin Account ===")
        login_username = input("Set admin username: ")
        login_password = input("Set admin password: ")
        try:
            with open("admin.txt", "w") as admin_file:
                admin_file.write(f"{login_username}|{login_password}\n")
            with open("admin.txt", "a") as adminfile:
                adminfile.write("verified")
            print("Admin account created and verified!")
        except IOError as e:
            print("Failed to create admin account:", e)
            return False
        return True
    else:
        # Login if setup is already there
        try:
            with open("admin.txt", "r") as admin_file:
                stored = admin_file.read().strip().split("|")
                if len(stored) == 2:
                    login_username, login_password = stored
        except IOError as e:
            print("Error reading admin file:", e)
            return False

        print("=== Admin Login ===")
        username = input("Enter username: ")
        password = input("Enter password: ")
        if username == login_username and password == login_password:
            print("Admin login successful!")
            try:
                with open("admin.txt", "a") as adminfile:
                    adminfile.write("verified")
            except IOError:
                print("Warning: Could not create verification file.")
            return True
        else:
            print("Admin login failed.")
            return False

# Start the app
def start_app():
    load_accounts()
    print("=== Welcome to Mini Banking App ===")

    if not admin_setup_or_login():
        print("Admin login/setup failed. Exiting app.")
        return

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
            print("Exiting app. Goodbye!")
            break
        else:
            print("Invalid option.")

# Run the application
start_app()














































                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
            
            

