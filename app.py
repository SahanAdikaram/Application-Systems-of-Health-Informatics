from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect  # Import the Inspector

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publication_year = db.Column(db.Integer, nullable=False)

# Route to display list of books
@app.route('/books')
def books():
    try:
        all_books = Book.query.all()
        return render_template('books.html', books=all_books)
    except Exception as e:
        return str(e)

# Route to add a new book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            title = request.form['title']
            author = request.form['author']
            publication_year = request.form['publication_year']

            new_book = Book(title=title, author=author, publication_year=publication_year)

            db.session.add(new_book)
            db.session.commit()

            return redirect(url_for('books'))
        except Exception as e:
            db.session.rollback()  # Rollback changes if an error occurs
            return str(e)

    return render_template('add_book.html')

if __name__ == '__main__':
    # Check if the 'book' table exists before creating it
    with app.app_context():
        inspector = inspect(db.engine)
        if not inspector.has_table('book'):
            db.create_all()
    app.run(debug=True)
