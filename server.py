from flask import Flask, g, render_template, request
from datetime import datetime
import sqlite3

app = Flask(__name__)

DATABASE = 'Instance/site2.db'

# db helper
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

@app.route('/')
@app.route('/home')
def home():
	cursor = get_db().cursor()
	cursor.execute('SELECT * FROM books')
	books = cursor.fetchall()
	cursor.close()
      
	return render_template('home.html', books=books)
      
@app.route('/books')
def books():
	cursor = get_db().cursor()
	cursor.execute('SELECT * FROM books')
	books = cursor.fetchall()
	cursor.close()

	return render_template('books.html', books=books)

@app.route('/bookCreate', methods=['POST', 'GET'])
def bookCreate():
	msg = ""
	if request.method == 'POST':
		try:
			title = request.form['title']
			author = request.form['author']
			date_published = datetime.now().strftime('%d-%m-%Y')
			with get_db() as connect:
				cursor = connect.cursor()
				cursor.execute(
                    "INSERT INTO books (title, author, date_published) VALUES (?, ?, ?)",
                    (title, author, date_published)
                )
				connect.commit()
			msg = "Record successfully added"
		except:
			connect.rollback()
			msg = f"Error in insert opperation"
		finally:
			return render_template("books.html", msg=msg)
	return render_template("bookCreate.html", msg=msg)


@app.route('/about')
def about():
	return render_template('about.html')


if __name__ == '__main__':
	app.run(debug=True)