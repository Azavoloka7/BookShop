# bookshop_classes.py

class Book:
    def __init__(self, book_id, title, author, price):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.price = price

    def display_info(self):
        print(f"ID: {self.book_id}, Title: {self.title}, Author: {self.author}, Price: {self.price}")


class Client:
    def __init__(self, client_id, name, email):
        self.client_id = client_id
        self.name = name
        self.email = email

    def display_info(self):
        print(f"ID: {self.client_id}, Name: {self.name}, Email: {self.email}")


class Manager:
    def __init__(self, manager_id, username, email):
        self.manager_id = manager_id
        self.username = username
        self.email = email

    def display_info(self):
        print(f"ID: {self.manager_id}, Username: {self.username}, Email: {self.email}")
