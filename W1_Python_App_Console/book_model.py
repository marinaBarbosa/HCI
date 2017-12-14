import sys
import sqlite3

class BookModel(object):
    def __init__(self):
        
        # Create a database in RAM
        self._db = sqlite3.connect(':memory:')
        self._db.row_factory = sqlite3.Row

        # Create the basic contact table.
        self._db.cursor().execute('''
            CREATE TABLE books(
                id INTEGER PRIMARY KEY,
                title TEXT,
                author TEXT,
                price TEXT,
                stock TEXT)
        ''')
        self._db.commit()

        # Current books when editing.
        self.current_id = None

    def add(self, books):
        self._db.cursor().execute('''
            INSERT INTO books(title, author, price, stock)
            VALUES(:title, :author, :price, :stock)''',
                                  books)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT title, id from books").fetchall()

    def get_contact(self, book_id):
        return self._db.cursor().execute(
            "SELECT * from books WHERE id=:id", {"id": book_id}).fetchone()

    def get_current_book(self):
        if self.current_id is None:
            return {"title": "", "author": "", "price": "", "stock": ""}
        else:
            return self.get_contact(self.current_id)

    def update_current_book(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
                UPDATE books SET title=:title, author=:author, price=:price, stock=:stock WHERE id=:id''',
                                      details)
            self._db.commit()

    def delete_book(self, book_id):
        self._db.cursor().execute('''
            DELETE FROM books WHERE id=:id''', {"id": book_id})
        self._db.commit()
