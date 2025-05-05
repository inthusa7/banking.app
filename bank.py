#Function  deposit money into  an account
def deposit_money():
    acc_no = input("Enter account number:")
    if acc_no not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input("Enter amount to deposit:")) 
        if amount<=0:
            print("Deposite amount must be positive.")  
            return

    accounts[acc_no]['balance'] += amount
    accounts[acc_no]['transactions'].append("Deposited:{amount}")
    print("Deposit successfuly")


#Function withdraw money from an account
def withdraw_money():
    acc_no = input("Enter account number:")
    if acc_no not in accounts:
        print("Account not found.")
        return
    try:
        amount = float(input("Enter amount to withdraw:"))
        if    






































                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             


def main_menu():
    while True:
        admin_name=input("Enter your password:")
        admin_password=int(input("Enter your password:"))
        if admin_name==user_name and user_password==admin_password:
            print("login succesfully")
            print("1.Customer Create")
            print("2.Create admin")
            print("3.Deposit Money")
            print("4.withdraw Money")
            print("5.Check Balance")
            print("6.Transaction History")
            print("7.Exit")
    while True:
            choice=input("Choose an option(1-7):")
            
            

