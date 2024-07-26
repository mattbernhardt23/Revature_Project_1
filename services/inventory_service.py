import os
import mysql.connector
from mysql.connector import Error
import bcrypt
from decimal import Decimal
from tabulate import tabulate
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

db_config = {
    "host": os.environ.get("MYSQL_HOST"),
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DB")
}

def get_inventory():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Select all books from the inventory
        query = "SELECT product_id, title, author, year_published, description, sales_price, stock_quantity FROM inventory"
    
        cursor.execute(query)

        # Fetch all the results
        books = cursor.fetchall()

        # Return the books
        return books

    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def buy_book(username):
    try:
        product_id = int(input("Enter the Id of the book you want to buy: "))
        
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Select the book from the inventory
        query = "SELECT product_id, title, author, year_published, description, sales_price, stock_quantity FROM inventory WHERE product_id = %s"
        cursor.execute(query, (product_id,))

        # Fetch the result
        book = cursor.fetchone()

        # Check if the book exists
        if book:
            # Check if the quantity requested is available
            if book[6] >= 1:
                # Calculate the total price
                total_price = book[5] * 1

                # Ask the user to confirm the purchase
                print(f"Title: {book[1]}")
                print(f"Author: {book[2]}")
                print(f"Price: ${book[5]}")
                print(f"Quantity: {1}")
                print(f"Total Price: ${total_price}")
                print("")
                confirm = input("Confirm Purchase? (Y/N): ")

                if confirm.lower() == "y":
                    # Update the stock quantity
                    new_quantity = book[6] - 1
                    insert_query = """
                        INSERT INTO orders (username, product_id, total_amount)
                        VALUES (%s, %s, %s)
                         """
                    cursor.execute(insert_query, (username, product_id, total_price))

                    # Insert Into Orders Table
                    order_query = "INSERT INTO orders (username, product_id, total_amount) VALUES (%s, %s, %s)"
                    order_values = (username, product_id, total_price)
                    # Execute the queries
                    cursor.execute(order_query, order_values)

                    # Update Customers Table with New Account Balance
                    update_query = "UPDATE customers SET account_balance = account_balance - %s WHERE username = %s"
                    update_values = (total_price, username)
                    cursor.execute(update_query, update_values)

                    # Update the stock quantity
                    update_query = "UPDATE inventory SET stock_quantity = %s WHERE product_id = %s" 
                    update_values = (new_quantity, product_id)
                    cursor.execute(update_query, update_values)

                    # Update Balance in Admin
                    update_query = "UPDATE customers SET account_balance = account_balance - %s WHERE admin = %s"
                    total_price = total_price * -1
                    update_values = (total_price, True)
                    cursor.execute(update_query, update_values)

                    # Commit the transaction
                    db.commit()

                    print("Purchase Successful!")
                    print("")
                    return total_price
                else:
                    print("Purchase Cancelled.")
                    print("")
            else:
                print("Insufficient Stock.")
                print("")
        else:
            print("Book not found.")
            print("")

    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def read_description(books):
    # Take Input from User Regarding Id of Book
    product_id = int(input("Enter the Id of the book you want to read the description of: "))
    
    # Iterate Over Books and Print Description of Book
    for book in books:
        if book[0] == product_id:
            print(f"Title: {book[1]}")
            print(f"Author: {book[2]}")
            print(f"Description: {book[4]}")
            return
        
    print("Book not found.")

def add_book():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user to enter the book details
        title = input("Enter the title of the book: ")
        author = input("Enter the author of the book: ")
        year_published = int(input("Enter the year the book was published: "))
        description = input("Enter a description of the book: ")
        sales_price = Decimal(input("Enter the sales price of the book: "))
        product_cost = Decimal(input("Enter the cost of the book: "))
        stock_quantity = int(input("Enter the stock quantity of the book: "))


        # Insert the book into the inventory
        query = """
            INSERT INTO inventory (title, author, year_published, description, sales_price, product_cost, stock_quantity)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = (title, author, year_published, description, sales_price, product_cost, stock_quantity)

        # Execute the query
        cursor.execute(query, values)

        # Commit the transaction
        db.commit()

        print("Book added successfully!")
        print("")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close() 

def remove_book():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user for the product_id of the book to remove
        product_id = int(input("Enter the Id of the book you want to remove: "))

        # Check if the book exists
        query = "SELECT * FROM inventory WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        book = cursor.fetchone()

        if book:
            # Delete the book from the inventory
            delete_query = "DELETE FROM inventory WHERE product_id = %s"
            cursor.execute(delete_query, (product_id,))

            # Commit the transaction
            db.commit()

            print("Book removed successfully!")
            print("")
        else:
            print("Book not found.")
            print("")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()  

def add_to_inventory():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user for the product_id of the book to add stock
        product_id = int(input("Enter the Id of the book you want to add stock to: "))

        # Check if the book exists
        query = "SELECT * FROM inventory WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        book = cursor.fetchone()

        if book:
            # Ask the user for the quantity to add
            quantity = int(input("Enter the quantity to add: "))

            # Update the stock quantity
            new_quantity = book[6] + quantity
            update_query = "UPDATE inventory SET stock_quantity = %s WHERE product_id = %s"
            update_values = (new_quantity, product_id)

            # Execute the query
            cursor.execute(update_query, update_values)

            # Commit the transaction
            db.commit()

            print("Stock added successfully!")
            print("")
        else:
            print("Book not found.")
            print("")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()

def print_inventory(books):
    # Extract only the title, author, and price from the books data
    book_data = [(book[0], book[1], book[2], book[5], book[6]) for book in books]
    # Define headers for the table
    headers = ["Id", "Title", "Author", "Price", "Stock Quantity"]
    # Print the table
    print(tabulate(book_data, headers=headers, floatfmt=".2f", tablefmt="pretty"))
    print("")

def get_stats():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Get the total sales
        total_sales_query = "SELECT SUM(total_amount) FROM orders"
        cursor.execute(total_sales_query)
        total_sales = cursor.fetchone()[0]

        # Get the total number of orders
        total_orders_query = "SELECT COUNT(*) FROM orders"
        cursor.execute(total_orders_query)
        total_orders = cursor.fetchone()[0]

        # Get the total number of customers
        total_customers_query = "SELECT COUNT(*) FROM customers"
        cursor.execute(total_customers_query)
        total_customers = cursor.fetchone()[0]

        # Get the total number of books in the inventory
        total_books_query = "SELECT SUM(stock_quantity) FROM inventory"
        cursor.execute(total_books_query)
        total_books = cursor.fetchone()[0]

        # Return the Top 5 Selling Books
        top_books_query = """
            SELECT inventory.title, inventory.author, SUM(orders.total_amount) AS total_sales
            FROM inventory
            JOIN orders ON inventory.product_id = orders.product_id
            GROUP BY inventory.product_id
            ORDER BY total_sales DESC
            LIMIT 5
        """
        cursor.execute(top_books_query)
        top_books = cursor.fetchall()

        # Get the total amount of money in the inventory
        total_inventory_query = "SELECT SUM(sales_price * stock_quantity) FROM inventory"
        cursor.execute(total_inventory_query)
        total_inventory = cursor.fetchone()[0]

        # Print the statistics
        print(f"Total Sales: ${total_sales}")
        print(f"Total Orders: {total_orders}")
        print(f"Total Customers: {total_customers}")
        print(f"Total Books: {total_books}")
        print(f"Total Inventory Value: ${total_inventory}")
        print("Top Selling Books:")
        print(tabulate(top_books, headers=["Title", "Author", "Total Sales"], floatfmt=".2f", tablefmt="pretty"))
        print("")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()