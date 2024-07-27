import os
import mysql.connector
from mysql.connector import Error
import bcrypt
from decimal import Decimal
from tabulate import tabulate
from dotenv import load_dotenv
import logging

load_dotenv()  # Load environment variables from .env file

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log")
    ]
)

db_config = {
    "host": os.environ.get("MYSQL_HOST"),
    "user": os.environ.get("MYSQL_USER"),
    "password": os.environ.get("MYSQL_PASSWORD"),
    "database": os.environ.get("MYSQL_DB")
}


def register():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database for user registration")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user for input
        username = input("Enter your username: ")
        while True:
            password = input("Enter your password: ")
            confirm_password = input("Confirm your password: ")
            admin = False

            if password == confirm_password:
                # Hash the password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                break
            else:
                print("Passwords do not match. Please try again.")

        # Insert the new user into the database
        query = "INSERT INTO customers (username, password, admin) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, hashed_password, admin))
        logging.info(f"Executed query to register user: {username}")

        # Commit the transaction
        db.commit()
        logging.info("Transaction committed for user registration")

        print("User registered successfully!")
        user = {
            "username": username,
            "account_balance": 0,
            "admin": admin
        }
        # Return a user object
        return user 

    except Error as e:
        logging.error(f"Error during user registration: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection after user registration")


def sign_in():
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database for user sign-in")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user for input
        username = input("Enter your username: ")
        password = input("Enter your password: ")

        # Query the user in the database
        query = "SELECT username, password, account_balance, admin FROM customers WHERE username = %s"
        cursor.execute(query, (username,))
        logging.info(f"Executed query to sign in user: {username}")
        result = cursor.fetchone()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[1].encode('utf-8')):
            logging.info(f"User signed in successfully: {username}")
            print("User signed in successfully!")
            user = {
                "username": result[0],
                "account_balance": result[2],
                "admin": result[3]
            }
            return user
        else:
            logging.warning(f"Invalid username or password for user: {username}")
            print("Invalid username or password.")
            return None

    except Error as e:
        logging.error(f"Error during user sign-in: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection after user sign-in")


def add_money(username):
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database to add money")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Ask the user for the amount to add
        while True:
            try:
                amount = float(input("Enter the amount of money you want to add (max 100,000): "))
                if amount > 0 and amount <= 100000:
                    amount = Decimal(amount)
                    break
                else:
                    print("Invalid amount. Please enter a value between 1 and 100,000.")
            except ValueError:
                print("Invalid input. Please enter a numeric value.")

        # Update the user's account balance
        query = "UPDATE customers SET account_balance = account_balance + %s WHERE username = %s"
        cursor.execute(query, (amount, username))
        logging.info(f"Executed query to add money to user account: {username}")

        # Commit the transaction
        db.commit()
        logging.info("Transaction committed for adding money")

        print(f"{amount} has been added to your account successfully!")
        return amount

    except Error as e:
        logging.error(f"Error adding money to account for user: {username}, Error: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection after adding money")


def get_library(username):
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database to get user library")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Select the books in the user's library
        query = """
            SELECT DISTINCT inventory.title, inventory.author
            FROM inventory
            JOIN orders ON inventory.product_id = orders.product_id
            JOIN customers ON orders.username = customers.username
            WHERE customers.username = %s;
            """
        cursor.execute(query, (username,))
        logging.info(f"Executed query to get library for user: {username}")

        # Fetch all the results
        library = cursor.fetchall()

        # Return the library
        return library

    except Error as e:
        logging.error(f"Error getting library for user: {username}, Error: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection after getting library")


def print_library(library):
    if library:
        # Extract only the title and author from the books data
        book_data = [(book[0], book[1]) for book in library]
        # Define headers for the table
        headers = ["Title", "Author"]
        # Print the table
        print(tabulate(book_data, headers=headers, floatfmt=".2f", tablefmt="pretty"))
    else:
        print("Your library is empty.")


def get_account_balance(username):
    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(**db_config)
        logging.info("Connected to the database to get account balance")

        # Create a cursor object to execute SQL queries
        cursor = db.cursor()

        # Select the user's account balance
        query = "SELECT account_balance FROM customers WHERE username = %s"
        cursor.execute(query, (username,))
        logging.info(f"Executed query to get account balance for user: {username}")
        result = cursor.fetchone()

        # Return the account balance
        return result[0]

    except Error as e:
        logging.error(f"Error getting account balance for user: {username}, Error: {e}")
        return None
    finally:
        if db.is_connected():
            cursor.close()
            db.close()
            logging.info("Closed the database connection after getting account balance")
