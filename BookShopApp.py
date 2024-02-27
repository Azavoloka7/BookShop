import mysql.connector
from datetime import datetime

# Connect to MySQL
def connect_to_database():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Z@v010ka",
            database="bookshop",
            port="3308"
        )
        return mydb, mydb.cursor()
    except mysql.connector.Error as e:
        print("Error connecting to the database:", e)
        return None, None

# Function to execute SQL query
def execute_query(cursor, query, data=None, fetch_result=False):
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        
        if fetch_result:
            return cursor.fetchall()
        else:
            return True
    except mysql.connector.Error as err:
        print("Error executing query:", err)
        return False


# Function to display books
def display_books(cursor):
    query = "SELECT * FROM books"
    if execute_query(cursor, query):
        books_data = cursor.fetchall()
        if books_data:
            print("\n=====================================")
            print("           Available Books           ")
            print("=====================================")
            print("ID    | Title               | Author")
            print("-------------------------------------")
            for book_data in books_data:
                print(f"{book_data[0]:<6} | {book_data[1]:<20} | {book_data[2]}")
            print("-------------------------------------")
        else:
            print("No books found.")
    else:
        print("Error fetching books.")

# Function to add a new book
def add_new_book(cursor):
    title = input("Enter book title: ")
    author = input("Enter book author: ")
    price = float(input("Enter book price: "))
    query = "INSERT INTO books (title, author, price) VALUES (%s, %s, %s)"
    if execute_query(cursor, query, (title, author, price)):
        mydb.commit()
        print("New book added successfully.")

# Function to display clients
def display_clients(cursor):
    query = "SELECT id, name, email, balance FROM clients"
    if execute_query(cursor, query):
        clients_data = cursor.fetchall()
        print("\n=====================================")
        print("               Clients               ")
        print("=====================================")
        print("ID    | Name                | Email")
        print("-------------------------------------")
        for client_data in clients_data:
            print(f"{client_data[0]:<6} | {client_data[1]:<20} | {client_data[2]}")
        print("-------------------------------------")

# Function to add a new client
def add_new_client(cursor):
    client_name = input("Enter client name: ")
    client_email = input("Enter client email: ")
    query = "INSERT INTO clients (name, email) VALUES (%s, %s)"
    if execute_query(cursor, query, (client_name, client_email)):
        mydb.commit()
        print("New client added successfully.")

# Function to display managers
def display_managers(cursor):
    query = "SELECT * FROM managers"
    if execute_query(cursor, query):
        managers_data = cursor.fetchall()
        print("\n=====================================")
        print("              Managers               ")
        print("=====================================")
        print("ID    | Name                | Email")
        print("-------------------------------------")
        for manager_data in managers_data:
            print(f"{manager_data[0]:<6} | {manager_data[1]:<20} | {manager_data[2]}")
        print("-------------------------------------")

# Function to add a new manager
def add_new_manager(cursor):
    manager_name = input("Enter manager name: ")
    manager_email = input("Enter manager email: ")
    query = "INSERT INTO managers (name, email) VALUES (%s, %s)"
    if execute_query(cursor, query, (manager_name, manager_email)):
        mydb.commit()
        print("New manager added successfully.")

# Function to sell book to client
def sell_book_to_client(mydb, cursor):
    book_id = input("Enter book ID: ")
    client_id = input("Enter client ID: ")
    manager_id = input("Enter manager ID: ")
    
    # Check if the book exists
    query_select_book = "SELECT * FROM books WHERE id = %s"
    if not execute_query(cursor, query_select_book, (book_id,), fetch_result=True):
        print("Error executing query: Book does not exist.")
        return
    
    # Check if the manager exists
    query_select_manager = "SELECT * FROM managers WHERE id = %s"
    if not execute_query(cursor, query_select_manager, (manager_id,), fetch_result=True):
        print("Error executing query: Manager does not exist.")
        return
    
    # Sell the book to the client
    query_select_book_price = "SELECT price FROM books WHERE id = %s"
    query_select_client_balance = "SELECT balance FROM clients WHERE id = %s"
    book_price = execute_query(cursor, query_select_book_price, (book_id,), fetch_result=True)[0][0]
    client_balance = execute_query(cursor, query_select_client_balance, (client_id,), fetch_result=True)[0][0]
    
    if client_balance >= book_price:
        new_balance = client_balance - book_price
        query_update_balance = "UPDATE clients SET balance = %s WHERE id = %s"
        if execute_query(cursor, query_update_balance, (new_balance, client_id)):
            # Insert transaction record
            query_insert_transaction = "INSERT INTO transactions (client_id, book_id, manager_id, transaction_date) VALUES (%s, %s, %s, %s)"
            transaction_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            execute_query(cursor, query_insert_transaction, (client_id, book_id, manager_id, transaction_date))
            mydb.commit()
            
            # Update manager sales count
            query_update_sales_count = "UPDATE managers SET sales_count = sales_count + 1 WHERE id = %s"
            execute_query(cursor, query_update_sales_count, (manager_id,))
            mydb.commit()
            
            print("Book sold successfully.")
    else:
        print("Client does not have enough balance to buy the book.")


# Function to display all transactions
def display_transactions(cursor):
    query = "SELECT transactions.id, clients.name, books.title, managers.name, transactions.transaction_date FROM transactions JOIN clients ON transactions.client_id = clients.id JOIN books ON transactions.book_id = books.id JOIN managers ON transactions.manager_id = managers.id"
    if execute_query(cursor, query):
        transactions_data = cursor.fetchall()
        if transactions_data:
            print("\n=====================================")
            print("             Transactions             ")
            print("=====================================")
            print("ID    | Client              | Book                | Manager          | Date")
            print("--------------------------------------------------------------------------------")
            for transaction_data in transactions_data:
                transaction_date = transaction_data[4]
                formatted_date = transaction_date.strftime("%Y-%m-%d %H:%M:%S") if transaction_date else "N/A"
                print(f"{transaction_data[0]:<6} | {transaction_data[1]:<20} | {transaction_data[2]:<20} | {transaction_data[3]:<16} | {formatted_date}")
            print("--------------------------------------------------------------------------------")
        else:
            print("No transactions found.")
    else:
        print("Error fetching transactions.")

# Function to display books bought by a client
def display_books_by_client(cursor):
    client_id = input("Enter client ID: ")
    query = "SELECT books.id, books.title, books.author, books.price FROM books INNER JOIN transactions ON books.id = transactions.book_id WHERE transactions.client_id = %s"
    if execute_query(cursor, query, (client_id,)):
        books_data = cursor.fetchall()
        if books_data:
            print("\n=====================================")
            print(f"Books bought by client with ID {client_id}:")
            print("=====================================")
            print("ID    | Title               | Author            | Price")
            print("-------------------------------------")
            for book_data in books_data:
                print(f"{book_data[0]:<6} | {book_data[1]:<20} | {book_data[2]:<18} | ${book_data[3]}")
            print("-------------------------------------")
        else:
            print(f"No books bought by client with ID {client_id}.")

# Main function
def main():
    mydb, cursor = connect_to_database()
    if mydb and cursor:
        while True:
            print("\n=====================================")
            print("       Welcome to BookShop           ")
            print("=====================================")
            print("1. Display Books")
            print("2. Add Book")
            print("3. Add Client")
            print("4. Add Manager")
            print("5. Display Clients")
            print("6. Display Managers")
            print("7. Sell Book to Client")
            print("8. Display Books Bought by Client")
            print("9. Show All Transactions")
            print("0. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                display_books(cursor)
            elif choice == '2':
                add_new_book(cursor)
            elif choice == '3':
                add_new_client(cursor)
            elif choice == '4':
                add_new_manager(cursor)
            elif choice == '5':
                display_clients(cursor)
            elif choice == '6':
                display_managers(cursor)
            elif choice == '7':
                sell_book_to_client(mydb, cursor)
            elif choice == '8':
                display_books_by_client(cursor)
            elif choice == '9':
                display_transactions(cursor)
            elif choice == '0':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please try again.")
    else:
        print("Unable to establish database connection.")

if __name__ == "__main__":
    main()
