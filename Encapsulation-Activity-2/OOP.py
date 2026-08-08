class BankAccount:
    def __init__(self, account_number, account_name): #, passcode
        self.account_number = account_number
        self.account_name = account_name
        
       # self.__passcode = passcode  # Private attribute for security
        self.balance = 0
        
        
        
    def _show_balance(self):
        print("\nBalance: ₱" + str(self.balance))

    def __update_balance(self, amount):
        self.balance += amount

    def verify_credentials(self, acc_num,name ): #, passcode 
        return   self.account_number == acc_num and self.account_name == name#and self.__passcode == passcode

    def deposit(self, amount): #passcode, name, acc_num, 
        #if not self.verify_credentials(acc_num,name ): #, passcode
         #   print("\n[ERROR] Access Denied: Incorrect credentials!")
          #  return False
        if amount <= 0:
            print("\n[ERROR] Invalid deposit amount!")
            return False
        
        self.__update_balance(amount)
        #print("\n" + str(amount) )
        return True
def run_banking_system():
    print(" BANK SYSTEM ")
    #print("Please register a new account to begin.")
    
    # Registration Phase
    #try:
    acc_num = float(input("Enter Account Number: "))   
    
    #except ValueError:
    #    print("\n[ERROR] Please enter a valid number for Account Number.")
        
    #try:
    name = str(input("Enter Account Name: "))
    
    #except ValueError:
    #    print("\n[ERROR] Please enter a String.")
    
    #passcode = input("Create Passcode: ")
        
    # Instantiate the account
    account = BankAccount(acc_num,name  )#,passcode
    #print("\n[SUCCESS] Account registered for " + account.account_name + "!")
    #print("Account Number: " + account.account_number)
    #print("Initial sign-up bonus: $1000.00 added.")

    # Main Interface Loop
    while True:
        print("\n")
        #print(" BANK MENU - Logged in as: " + account.account_name)
        #print("===================================")
        print("1. Deposit ")
        print("2. Check Balance")
        print("3. Account Information")
        print("4. Exit ")
        #print("===================================")
        
        choice = input("Choose option : ")
        
        
            
        if choice == "1":
            print("\n--- DEPOSIT TRANSACTION ---")
            #v_name = input("Confirm Account Name: ")
            #v_num = input("Confirm Account Number: ")
            #v_pass = input("Verify Passcode: ")
            try:
                v_amount = float(input("Enter Deposit Amount: ₱"))
                if account.deposit(v_amount): #v_pass,
                    #account._show_balance()
                    print("\nDeposit Successfull")
            except ValueError:
                print("\n[ERROR] Please enter a valid number for the amount.")
                
        elif choice == "2":
            #print("Current Balance: ") 
            account._show_balance()
        
        elif choice == "3":
            print("\n--- ACCOUNT INFORMATION ---")
            
            print("Account Number: " + account.account_number)
            print("\nAccount Name: " + account.account_name )
            account._show_balance()
       # elif choice == "3":
        #    print("\n--- WITHDRAWAL TRANSACTION ---")
         #   v_name = input("Confirm Account Name: ")
          #  v_num = input("Confirm Account Number: ")
           # v_pass = input("Verify Passcode: ")
            #try:
             #   v_amount = float(input("Enter Withdrawal Amount: $"))
              #  if account.withdraw(v_name, v_num, v_pass, v_amount):
               #     account._show_balance()
            #except ValueError:
             #   print("\n[ERROR] Please enter a valid number for the amount.")
                
        elif choice == "4":
            print("\nThank you for using Bank System")
            break
            
        else:
            print("\n[ERROR] Invalid menu choice. Please select 1, 2, 3, or 4.")


# Run the application directly
run_banking_system()