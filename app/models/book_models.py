from .database import db_connection

class BookModel:
    @db_connection
    def get_all_books(self, cursor):
        cursor.execute('SELECT * FROM books')
        return cursor.fetchall()
    
    @db_connection
    def get_book_by_id(self, cursor, book_id):
        cursor.execute('SELECT * FROM books WHERE id = ?', [book_id])
        return cursor.fetchone()
    
    @db_connection
    def insert_book(self, cursor, title, author, date_published):
        cursor.execute(
            "INSERT INTO books (title, author, date_published) VALUES (?, ?, ?)", 
            (title, author, date_published)
        )
    
    @db_connection
    def update_book(self, cursor, book_id, title, author):
        cursor.execute(
            "UPDATE books SET title = ?, author = ? WHERE id = ?",
            (title, author, book_id)
        )
    
    @db_connection
    def delete_book(self, cursor, book_id):
        cursor.execute('DELETE FROM books WHERE id = ?', [book_id])