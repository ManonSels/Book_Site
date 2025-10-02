import sqlite3

class DBConnection:
    def __enter__(self):
        self.conn = sqlite3.connect('Instance/site2.db')
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            if exc_type is None:
                self.conn.commit()
            self.conn.close()
        return False

def db_connection(func):
    def wrapper(self, *args, **kwargs):
        with DBConnection() as cursor:
            result = func(self, cursor, *args, **kwargs)
            return result
    return wrapper