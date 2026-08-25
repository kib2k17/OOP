class BankAccount:

    # Make sure all 5 parameters are listed here:
    def __init__(self, account_number, account_name, account_type, initial_bal):
        self.__account_number = account_number
        self.__account_name = account_name
        self.__account_type = account_type
        self.__initial_bal = initial_bal
        self.__balance = float(initial_bal)

        

    def get_account_number(self):
        return self.__account_number

    def get_account_name(self):
        return self.__account_name

    def get_account_type(self):
        return self.__account_type
        
    def get_balance(self):
        return self.__balance
         
        
    def __update_balance(self, amount):
        self.__balance += amount


    def deposit(self, amount):
        if amount <= 0:
            print("\n[ERROR] Invalid deposit amount!")
            return False
        self.__update_balance(amount)
        return True
        
    def withdraw(self, amount):
        if amount <= 0:
            print("\n[ERROR] Invalid withdrawal amount!")
            return False
        if amount > self.__balance:
            print("\n[ERROR] Insufficient balance for this withdrawal.")
            return False
        self.__update_balance(-amount)
        return True

    @staticmethod
    def print_header(title, width=35):
        print("\n" + "=" * width)
        print(title.center(width))
        print("=" * width)

    def display_info(self):
        self.print_header("BANK ACCOUNT INFO")
        print(f"Account Number: {self.get_account_number()}")
        print(f"Account Name: {self.get_account_name()}")
        print(f"Account Type: {self.get_account_type()}")
        print(f"Balance: ₱{self.get_balance():.2f}")

    def perform_deposit(self):
        BankAccount.print_header("DEPOSIT TRANSACTION")
        try:
            v_amount = float(input("Enter Deposit Amount: ₱"))
            if self.deposit(v_amount):
                print("\nDeposit Successful")
                print(f"Current Balance: ₱{self.get_balance():.2f}")
        except ValueError:
            print("\n[ERROR] Please enter a valid number.")

    def perform_withdraw(self):
        BankAccount.print_header("WITHDRAWAL TRANSACTION")
        try:
            v_amount = float(input("Enter Withdraw Amount: ₱"))
            if self.withdraw(v_amount):
                print("\nWithdrawal Successful")
                print(f"Current Balance: ₱{self.get_balance():.2f}")
        except ValueError:
            print("\n[ERROR] Please enter a valid number.")