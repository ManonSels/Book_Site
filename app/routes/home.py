from flask import Blueprint, render_template
from app.models.book_models import BookModel

bp = Blueprint('home', __name__)

@bp.route('/')
@bp.route('/home')
def home():
    book_model = BookModel()
    books = book_model.get_all_books()
    return render_template('home.html', books=books)
