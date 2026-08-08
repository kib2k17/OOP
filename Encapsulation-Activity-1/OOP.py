class BankAccount:
    def __init__(self,account_name,account_number, passcode):
        self.balance = 1000

    def _show_balance(self):
        print(f"Current Balance: {self.balance}")  # Protected method

    def __update_balance(self, amount):
        self.balance += amount             # Private method

    def deposit(self, amount):
        if amount > 0:
            self.__update_balance(amount)  # Accessing private method internally
            self._show_balance()           # Accessing protected method
        else:
            print("Invalid deposit amount!")
            
account = BankAccount()
#account._show_balance()      # Works, but should be treated as internal
# account.__update_balance(500)  # Error: private method
#account.deposit(500)         # Uses both methods internally

#account.deposit = input("Deposit: ")
account.deposit(int(input("Deposit: ")))
#account._show_balance()
#acc2 = BankAccount(y)

