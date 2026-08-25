class BankAccount:
    
    # Private attributes
    __account_number = ""
    __account_name = ""
    __balance = 0.0

    def __init__(self, account_number, account_name):
        self.__account_number = account_number
        self.__account_name = account_name
        self.__balance = 0.0

    # Getter methods
    def get_account_number(self):
        return self.__account_number

    def get_account_name(self):
        return self.__account_name

    def get_balance(self):
        return self.__balance

    # Private method for updating balance
    def __update_balance(self, amount):
        self.__balance += amount

    # Deposit method
    def deposit(self, amount):

        if amount <= 0:
            print("\n[ERROR] Invalid deposit amount!")
            return False

        self.__update_balance(amount)
        return True

    #Withdraw method
    def withdraw(self, amount):

        if amount <= 0:
            print("\n[ERROR] Invalid withdrawal amount!")
            return False
        if amount > self.__balance:
                    print("\n[ERROR] Insufficient balance for this withdrawal.")
                    return False
        self.__update_balance(-amount)
        return True

def run_banking_system():

    print(" BANK SYSTEM ")

    acc_num = int(input("Enter Account Number: "))
    name = str(input("Enter Account Name: "))

    account = BankAccount(acc_num, name)

    while True:

        print("\n")
        print("1. Deposit")
        print("2. Withdraw")
        print("3. Check Balance")
        print("4. Account Information")
        print("5. Exit")

        choice = input("Choose option: ")

        # Deposit
        if choice == "1":

            print("\n--- DEPOSIT TRANSACTION ---")

            try:
                v_amount = float(input("Enter Deposit Amount: ₱"))

                if account.deposit(v_amount):
                    print("\nDeposit Successful")

            except ValueError:
                print("\n[ERROR] Please enter a valid number for the amount.")

        elif choice == "2":
            print("\n--- WITHDRAWAL TRANSACTION ---")
            try:
                v_amount = float(input("Enter Withdraw Amount: ₱"))
                if account.withdraw(v_amount):
                    print("\nWithdrawal Successful")
                    print(f"Current Balance: ₱{account.get_balance():.2f}")
            except ValueError:
                    print("\n[ERROR] Please enter a valid number.")

        # Check Balance
        elif choice == "3":
            print("\n--- CHECK BALANCE ---")
            print("\nBalance: ₱" + str(account.get_balance()))

        # Account Information
        elif choice == "4":

            print("\n--- ACCOUNT INFORMATION ---")

            print("Account Number: " + str(account.get_account_number()))
            print("Account Name: " + account.get_account_name())
            print("Balance: ₱" + str(account.get_balance()))

        # Exit
        elif choice == "5":

            print("\nThank you for using Bank System")
            break

        # Invalid choice
        else:

            print(
                "\n[ERROR] Invalid menu choice. "
                "Please select 1, 2, 3, 4, or 5."
            )


run_banking_system()
