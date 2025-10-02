from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from app.models.book_models import BookModel

bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('/')
def books_list():
    book_model = BookModel()
    books = book_model.get_all_books()
    return render_template('books.html', books=books)

@bp.route('/create', methods=['GET', 'POST'])
def book_create():
    book_model = BookModel()
    
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            date_published = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            
            book_model.insert_book(title, author, date_published)
            flash("Record successfully added", "success")
            return redirect(url_for('books.book_create'))
            
        except Exception as e:
            flash(f"Error in insert operation: {str(e)}", "error")
    
    return render_template("bookCreate.html")

@bp.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def book_edit(book_id):
    book_model = BookModel()
    
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            
            book_model.update_book(book_id, title, author)
            flash("Book updated successfully", "success")
            return redirect(url_for('books.books_list'))
            
        except Exception as e:
            flash(f"Error updating book: {str(e)}", "error")
    
    book = book_model.get_book_by_id(book_id)
    if book is None:
        flash("Book not found", "error")
        return redirect(url_for('books.books_list'))
    
    return render_template('bookEdit.html', book=book)

@bp.route('/delete/<int:book_id>', methods=['POST'])
def book_delete(book_id):
    book_model = BookModel()
    
    try:
        book_model.delete_book(book_id)
        flash("Book deleted successfully", "success")
    except Exception as e:
        flash(f"Error deleting book: {str(e)}", "error")
    
    return redirect(url_for('books.books_list'))