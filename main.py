from models.user import User
from models.inventory import Inventory
from utils.book_shop import entering_book_shop
import logging
logger = logging.getLogger(__name__)

def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    logger.info('Started')
    logger.info('Finished')
    user = User()   

    while user.username == "":
        print("Welcome to Book World!")
        print("Please, Sign-In. If you are not a member, please Register.")
        print("")

        print("1.Sign-In")
        print("2.Register")
        print("3.Exit")
        print("")

        choice = input("Enter your choice: ")
        # create the logic that will allow the user to sign in or sign up   
        if choice == "1":
            print("Sign-In")
            result = user.sign_in()
        elif choice == "2":
            print("Register")
            result = user.register()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")
            continue

        if result:
            user.username = result["username"]
            user.account_balance = result["account_balance"]
        else:
            print("Failed to Sign-In/Register. Please try again.")

    # Get Inventory of Books
    inventory = Inventory()
    inventory.get_inventory() 
    books = inventory.books  

    if user.admin:
        print("Welcome Admin!")

        while True:
            print("")
            print("1. Add Book")
            print("2. Remove Book")
            print("3. View Inventory")
            print("4. Add to Inventory")
            print("5. View Stats")
            print("6. Get All Customers")
            print("7. Get All Orders")
            print("8. Exit")
            print("")

            choice = input("Enter your choice: ")
            print("")
            if choice == "1":
                inventory.add_book()
            elif choice == "2":
                inventory.remove_book()
            elif choice == "3":
                inventory.get_inventory()
                inventory.print_inventory()
            elif choice == "4":
                inventory.add_to_inventory()
            elif choice == "5":
                inventory.get_stats()
            elif choice == "6":
                inventory.get_customers()
            elif choice == "7":
                inventory.get_all_orders()
            elif choice == "8":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                continue
    else:
        # Present User with Menu to Either Buy Books, Add Money to Account, or Exit
        while True:
            user.get_account_balance()
            print("")
            print(f"Welcome {user.username}! Your account balance is ${user.account_balance}.")
            print("")
            print("1. Enter the Book Shop")
            print("2. Add Money")
            print("3. View Your Library")
            print("4. Exit")
            print("")

            choice = input("Enter your choice: ")
            print("")
            if choice == "1":
                entering_book_shop(books, user.username)
            elif choice == "2":
                user.add_money()
                print(f"Your new account balance is ${user.account_balance}.")
            elif choice == "3":
                user.get_library()
                user.print_library()
            elif choice == "4":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                continue

if __name__ == "__main__":
    main()
