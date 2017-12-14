import sys
import sqlite3

class ClientModel(object):
    def __init__(self):
        
        # Create a database in RAM
        self._db = sqlite3.connect(':memory:')
        self._db.row_factory = sqlite3.Row

        # Create the basic client table.
        self._db.cursor().execute('''
            CREATE TABLE clients(
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT,
                mobilephone TEXT)
        ''')
        self._db.commit()

        # Current clients when editing.
        self.current_id = None

    def add(self, clients):
        self._db.cursor().execute('''
            INSERT INTO clients(name, email, mobilephone)
            VALUES(:name, :email, :mobilephone)''',
                                  clients)
        self._db.commit()

    def get_summary(self):
        return self._db.cursor().execute(
            "SELECT name, id from clients").fetchall()

    def get_client(self, client_id):
        return self._db.cursor().execute(
            "SELECT * from clients WHERE id=:id", {"id": client_id}).fetchone()

    def get_current_client(self):
        if self.current_id is None:
            return {"name": "", "email": "", "mobilephone": ""}
        else:
            return self.get_client(self.current_id)

    def update_current_client(self, details):
        if self.current_id is None:
            self.add(details)
        else:
            self._db.cursor().execute('''
                UPDATE clients SET name=:name, email=:email, mobilephone=:mobilephone WHERE id=:id''',
                                      details)
            self._db.commit()

    def delete_client(self, client_id):
        self._db.cursor().execute('''
            DELETE FROM clients WHERE id=:id''', {"id": client_id})
        self._db.commit()