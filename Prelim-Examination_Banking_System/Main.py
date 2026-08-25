
from bank_account import BankAccount

class BankSystem:        
    
    @staticmethod
    def main():
        
        BankAccount.print_header("CREATE BANK ACCOUNT")
       

        acc_num = int(input("Enter Account Number: "))
        name = str(input("Enter Account Name: "))
        acc_type = str(input("Enter Account Type: "))
        init_bal = int(input("Enter Initial Balance: "))

       
        account = BankAccount(acc_num, name, acc_type, init_bal)
        print("\nAccount successfully created!\n")


        while True:
            
            BankAccount.print_header("BANK MENU")
            print("\n1. Display Account Information\n2. Deposit Money\n3. Withdraw Money\n4. Check Balance\n5. Exit")
            choice = input("Choose option: ")

            if choice == "1":
                account.display_info()


            
            elif choice == "2":
                account.perform_deposit()

            elif choice == "3":
                account.perform_withdraw()
                

            elif choice == "4":
                BankAccount.print_header("ACCOUNT BALANCE")
                print(f"Current Balance: ₱{account.get_balance():.2f}")


            elif choice == "5":
                BankAccount.print_header("SYSTEM EXIT")
                print("\nThank you for using the Bank Account Management System!\n")
                break
            else:
                print("\n[ERROR] Invalid menu choice.")

if __name__ == "__main__":
    BankSystem.main()