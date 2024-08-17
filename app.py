# app.py
from flask import Flask, render_template, url_for, flash, redirect, request
from config import Config
from datetime import datetime
from models import db, User, Book, Author, Category, BorrowedBook
from forms import RegistrationForm, LoginForm, AddBookForm, BorrowBookForm, ReturnBookForm
from flask_login import LoginManager, login_user, current_user, logout_user, login_required

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
@app.route("/home")
def home():
    books = Book.query.all()
    return render_template('home.html', books=books)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=form.password.data, role=form.role.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/add_book", methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.role != 'admin':
        flash('Only admins can add books', 'danger')
        return redirect(url_for('home'))
    
    form = AddBookForm()
    if form.validate_on_submit():
        author = Author.query.filter_by(name=form.author.data).first()
        if not author:
            author = Author(name=form.author.data)
            db.session.add(author)
        
        category = Category.query.filter_by(name=form.category.data).first()
        if not category:
            category = Category(name=form.category.data)
            db.session.add(category)

        book = Book(title=form.title.data, author=author, category=category, isbn=form.isbn.data, publication_date=form.publication_date.data)
        db.session.add(book)
        db.session.commit()
        flash('Book has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_book.html', form=form)

@app.route("/borrow_book", methods=['GET', 'POST'])
@login_required
def borrow_book():
    form = BorrowBookForm()
    if form.validate_on_submit():
        book = Book.query.get(form.book_id.data)
        if book and book.availability:
            borrowed_book = BorrowedBook(user_id=current_user.id, book_id=book.id)
            book.availability = False
            db.session.add(borrowed_book)
            db.session.commit()
            flash('You have borrowed the book!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Book is not available', 'danger')
    return render_template('borrow_book.html', form=form)

@app.route("/return_book", methods=['GET', 'POST'])
@login_required
def return_book():
    form = ReturnBookForm()
    if form.validate_on_submit():
        borrowed_book = BorrowedBook.query.filter_by(user_id=current_user.id, book_id=form.book_id.data, return_date=None).first()
        if borrowed_book:
            borrowed_book.return_date = datetime.utcnow()
            borrowed_book.book.availability = True
            db.session.commit()
            flash('You have returned the book!', 'success')
            return redirect(url_for('home'))
        else:
            flash('You have not borrowed this book', 'danger')
    return render_template('return_book.html', form=form)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
