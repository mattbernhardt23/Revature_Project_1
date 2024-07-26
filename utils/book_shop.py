from tabulate import tabulate
from services.inventory_service import buy_book, read_description

def entering_book_shop(books, username):
    print("You have entered the book shop!")
    # Extract only the title, author, and price from the books data
    book_data = [( book[0], book[1], book[2], book[5]) for book in books]
    # Define headers for the table
    headers = ["Id", "Title", "Author", "Price"]
    # Print the table
    print(tabulate(book_data, headers=headers, floatfmt=".2f", tablefmt="pretty"))
    print("")
    
    while True:
        print("What would you like to do?")
        print("1. Buy a Book")
        print("2. Read a Description")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            buy_book(username) 
        elif choice == "2":
            read_description(books)
        elif choice == "3":
            print("Exiting the book shop.")
            break

