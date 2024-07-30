import os
import mysql.connector
from mysql.connector import Error
from decimal import Decimal
from tabulate import tabulate
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log")
    ]
)

# Database configuration
db_config = {
    "host": os.environ.get("MYSQL_HOST"),
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DB")
}

# Retrieves Inventory from Database
# Returns: List of Tuples
def get_inventory():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Select all books from the inventory
        query = "SELECT product_id, title, author, year_published, description, sales_price, stock_quantity FROM inventory"
        cursor.execute(query)
        logging.info("Executed query to fetch inventory")

        # Fetch all the results
        books = cursor.fetchall()

        # Return the books
        return books

    except Error as e:
        logging.error(f"Error: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")

# Allows User to Purchase Books
def buy_book(username):
    try:
        product_id = int(input("Enter the Id of the book you want to buy: "))
        
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Select the book from the inventory
        query = "SELECT product_id, title, author, year_published, description, sales_price, stock_quantity FROM inventory WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        logging.info(f"Executed query to fetch book with product_id: {product_id}")

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
                    logging.info("Executed insert query to add order")


                    # Update Customers Table with New Account Balance
                    update_query = "UPDATE customers SET account_balance = account_balance - %s WHERE username = %s"
                    update_values = (total_price, username)
                    cursor.execute(update_query, update_values)
                    logging.info("Executed update query to adjust customer account balance")

                    # Update the stock quantity
                    update_query = "UPDATE inventory SET stock_quantity = %s WHERE product_id = %s" 
                    update_values = (new_quantity, product_id)
                    cursor.execute(update_query, update_values)
                    logging.info("Executed update query to adjust inventory stock quantity")

                    # Update Balance in Admin
                    update_query = "UPDATE customers SET account_balance = account_balance - %s WHERE admin = %s"
                    total_price = total_price * -1
                    update_values = (total_price, True)
                    cursor.execute(update_query, update_values)
                    logging.info("Executed update query to adjust admin account balance")

                    # Commit the transaction
                    db.commit()
                    logging.info("Transaction committed")

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
        logging.error(f"Error: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")

# Allows Users to Read Book Descrpition while Inside Book Store
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

# Admin Function: Add book to Inventory
def add_book():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

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
        logging.info(f"Executed insert query to add book: {title}")

        # Commit the transaction
        db.commit()
        logging.info("Transaction committed")

        print("Book added successfully!")
        print("")

    except Error as e:
        logging.error(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")

# Adming Function: Remove Book from Inventory
def remove_book():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user for the product_id of the book to remove
        product_id = int(input("Enter the Id of the book you want to remove: "))

        # Check if the book exists
        query = "SELECT * FROM inventory WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        logging.info(f"Executed select query to check if book with product_id: {product_id} exists")
        book = cursor.fetchone()

        if book:
            # Delete the book from the inventory
            delete_query = "DELETE FROM inventory WHERE product_id = %s"
            cursor.execute(delete_query, (product_id,))
            logging.info(f"Executed delete query to remove book with product_id: {product_id}")

            # Commit the transaction
            db.commit()
            logging.info("Transaction committed")

            print("Book removed successfully!")
            print("")
        else:
            print("Book not found.")
            print("")

    except Error as e:
        logging.error(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")

# Admin Function: Increases the Quantity of a Book in the Inventory
def add_to_inventory():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user for the product_id of the book to add stock
        product_id = int(input("Enter the Id of the book you want to add stock to: "))

        # Check if the book exists
        query = "SELECT * FROM inventory WHERE product_id = %s"
        cursor.execute(query, (product_id,))
        logging.info(f"Executed select query to check if book with product_id: {product_id} exists")
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
            logging.info(f"Executed update query to add {quantity} to stock of book with product_id: {product_id}")

            # Commit the transaction
            db.commit()
            logging.info("Transaction committed")

            print("Stock added successfully!")
            print("")
        else:
            print("Book not found.")
            print("")

    except Error as e:
        logging.error(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")

# Admin Function: Prints Inventory of Books
def print_inventory(books):
    # Extract only the title, author, and price from the books data
    book_data = [(book[0], book[1], book[2], book[5], book[6]) for book in books]
    # Define headers for the table
    headers = ["Id", "Title", "Author", "Price", "Stock Quantity"]
    # Print the table
    print(tabulate(book_data, headers=headers, floatfmt=".2f", tablefmt="pretty"))
    print("")

# Admin Function: Get Total Sales, Orders, Customers, Top Selling Books, and Inventory Value
def get_stats():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Get the total sales
        total_sales_query = "SELECT SUM(total_amount) FROM orders"
        cursor.execute(total_sales_query)
        logging.info("Executed query to get total sales")
        total_sales = cursor.fetchone()[0]

        # Get the total number of orders
        total_orders_query = "SELECT COUNT(*) FROM orders"
        cursor.execute(total_orders_query)
        logging.info("Executed query to get total number of orders")
        total_orders = cursor.fetchone()[0]

        # Get the total number of customers
        total_customers_query = "SELECT COUNT(*) FROM customers"
        cursor.execute(total_customers_query)
        logging.info("Executed query to get total number of customers")
        total_customers = cursor.fetchone()[0]

        # Get the total number of books in the inventory
        total_books_query = "SELECT SUM(stock_quantity) FROM inventory"
        cursor.execute(total_books_query)
        logging.info("Executed query to get total number of books in inventory")
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
        logging.info("Executed query to get top 5 selling books")
        top_books = cursor.fetchall()

        # Get the total amount of money in the inventory
        total_inventory_query = "SELECT SUM(sales_price * stock_quantity) FROM inventory"
        cursor.execute(total_inventory_query)
        logging.info("Executed query to get total inventory value")
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
        logging.error(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")

# Admin Function: Get All Customers
def get_customers():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Get all the customers
        query = "SELECT username, account_balance FROM customers"
        cursor.execute(query)
        logging.info("Executed query to get all customers")
        customers = cursor.fetchall()

        # Get the Number of Orders and Total Amount Spent for Each Customer
        for i, customer in enumerate(customers):
            orders_query = """
            SELECT COUNT(*), SUM(total_amount)
            FROM orders
            WHERE username = %s
            """
            cursor.execute(orders_query, (customer[0],))
            logging.info(f"Executed query to get number of orders and total amount spent for customer: {customer[0]}")
            result = cursor.fetchone()
            num_orders = result[0]
            total_spent = result[1] if result[1] is not None else 0  # Handle NULL total_amount case
            customers[i] = (customer[0], customer[1], num_orders, total_spent)


        # Print the customers
        print(tabulate(customers, headers=["Username", "Account Balance", "Number of Purchases", "Total Amount Spent"], floatfmt=".2f", tablefmt="pretty"))
        print("")

    except Error as e:
        logging.error(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")

# Admin Function: Get All Orders
def get_all_orders():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Get all the orders
        query = """
            SELECT orders.order_id, orders.username, inventory.title, orders.total_amount
            FROM orders
            JOIN inventory ON orders.product_id = inventory.product_id
        """
        cursor.execute(query)
        logging.info("Executed query to get all orders")
        orders = cursor.fetchall()

        # Print the orders
        print(tabulate(orders, headers=["Order Id", "Username", "Title", "Total Amount"], floatfmt=".2f", tablefmt="pretty"))
        print("")

    except Error as e:
        logging.error(f"Error: {e}")
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection")