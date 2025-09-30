from flask import Flask, g, render_template, request, redirect, url_for, flash
from datetime import datetime
import sqlite3

# ------------- END OF IMPORTS ------------- #

app = Flask(__name__)

app.secret_key = 'your-secret-key-here-make-it-very-long-and-random'
DATABASE = 'Instance/site2.db'

# ------------- DATABASE HELPER ------------- #


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# ------------- HOME ROUTE ------------- #


@app.route('/')
@app.route('/home')
def home():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    cursor.close()

    return render_template('home.html', books=books)


# ------------- BOOK DISPLAY ROUTE ------------- #

@app.route('/books')
def books():
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    cursor.close()

    return render_template('books.html', books=books)


# ------------- BOOK CREATE ROUTE ------------- #

@app.route('/bookCreate', methods=['POST', 'GET'])
def bookCreate():
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            date_published = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

            with get_db() as connect:
                cursor = connect.cursor()
                cursor.execute(
                    "INSERT INTO books (title, author, date_published) VALUES (?, ?, ?)",
                    (title, author, date_published)
                )
                connect.commit()

            flash("Record successfully added", "success")
            return redirect(url_for('bookCreate'))

        except Exception as e:
            flash(f"Error in insert operation: {str(e)}", "error")

    return render_template("bookCreate.html")


# ------------- BOOK EDIT ROUTE ------------- #

@app.route('/bookEdit/<int:book_id>', methods=['GET', 'POST'])
def bookEdit(book_id):
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            
            with get_db() as connect:
                cursor = connect.cursor()
                cursor.execute(
                    "UPDATE books SET title = ?, author = ? WHERE id = ?",
                    (title, author, book_id)
                )
                connect.commit()
            
            flash("Book updated successfully", "success")
            return redirect(url_for('books'))
            
        except Exception as e:
            flash(f"Error updating book: {str(e)}", "error")
    
    cursor = get_db().cursor()
    cursor.execute('SELECT * FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    cursor.close()
    
    if book is None:
        flash("Book not found", "error")
        return redirect(url_for('books'))
    
    return render_template('bookEdit.html', book=book)


# ------------- DELETE ROUTE ------------- #

@app.route('/bookDelete/<int:book_id>', methods=['POST', 'GET'])
def bookDelete(book_id):
    try:
        with get_db() as connect:
            cursor = connect.cursor()
            cursor.execute('DELETE FROM books WHERE id = ?', (book_id,))
            connect.commit()
        
        flash("Book deleted successfully", "success")
        
    except Exception as e:
        flash(f"Error deleting book: {str(e)}", "error")
    
    return redirect(url_for('books'))


# ------------- ABOUT ROUTE ------------- #


@app.route('/about')
def about():
    return render_template('about.html')



# ------------- END ------------- #

if __name__ == '__main__':
    app.run(debug=True)
