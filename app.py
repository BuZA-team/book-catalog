from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        year = int(request.form.get('year'))
        genre = request.form.get('genre')
        new_book = Book(title=title, author=author, year=year, genre=genre)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get(book_id)
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        book.year = int(request.form.get('year'))
        book.genre = request.form.get('genre')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', book=book)

@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    book = Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['GET', 'POST'])
def search_books():
    if request.method == 'POST':
        search_query = request.form.get('search_query')
        books = Book.query.filter(
            (Book.title.contains(search_query)) |
            (Book.author.contains(search_query)) |
            (Book.genre.contains(search_query))
        ).all()
        return render_template('index.html', books=books)
    return render_template('search.html')

@app.route('/update/<int:book_id>', methods=['POST'])
def update_book(book_id):
    book = Book.query.get(book_id)
    book.title = request.form.get('title')
    book.author = request.form.get('author')
    book.year = int(request.form.get('year'))
    book.genre = request.form.get('genre')
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)