from flask import render_template, flash, redirect, url_for, session
from app import db,app,bcrypt
from app.decarators import login_required
from app.forms import RegistrationForm, LoginForm, DeleteAccountForm, AddBookForm, DeleteBook
from app.models import User, Books


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["POST", "GET"])
@login_required(required=False)
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session["user_id"] = user.id
            session["username"] = user.username
            flash(f"Welcome {user.username}", "success")
            return redirect(url_for("home"))
        else:
            flash("username or password wrong", "danger")

    return render_template('auth/login.html', form=form)


@app.route("/register", methods=["POST", "GET"])
@login_required(required=False)
def register():

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        confirm_password_hesh = bcrypt.generate_password_hash(form.confirm_password.data).decode("utf-8")
        user = User(full_name=form.full_name.data, username=form.username.data, password=hashed_password,
                            email=form.email.data, confirm_password=confirm_password_hesh)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("auth/register.html",form=form)


@app.route("/add_book", methods=["POST", "GET"])
@login_required(required=True)
def add_book():
    form = AddBookForm()
    if form.validate_on_submit():
        book = Books(title=form.title.data, author=form.author.data, page_count=form.page_count.data, user_id=session["user_id"],)
        db.session.add(book)
        db.session.commit()
    return render_template("blogs/add-book.html", form=form)


@app.route("/delete_account", methods=["POST", "GET"])
@login_required(required=True)
def delete_account():
    form = DeleteAccountForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=session.get('user_id'), username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            User.query.filter_by(id=user.id).delete()
            db.session.commit()
            session.pop('username')
            session.pop('user_id')
            flash('You deleted account.But you can recover the account again.', 'info')
            return redirect(url_for('home'))
        else:
            flash('username or password is wrong!', 'danger')
    return render_template('blogs/delete-account.html', form=form)


@app.route("/delete_book", methods=["POST", "GET"])
@login_required(required=True)
def delete_book():
    form = DeleteBook()
    if form.validate_on_submit():
        book = Books.query.filter_by(id=session.get('book_id')).first()
        if Books.user_id == session.get('user_id'):
            Books.query.filter_by(id=book.id).delete()
            book.pop('title')
            book.pop('author')
            book.pop('page_count')
            db.session.commit()
        else:
            flash(error=401)
    return render_template('blogs/delete-book.html', form=form)


@app.route("/update_book", methods=["POST", "GET"])
@login_required(required=True)
def update_book(slug):
    book = Books.query.filter_by(slug=slug).first()
    form = AddBookForm()
    if form.validate_on_submit():
        book.title = form.title.data
        book.author = form.author.data
        book.page_count = form.page_count
        book.user_id = session.get('user_id')
        db.session.commit()
        flash("Book successfully updated", "success")
        return redirect(url_for("blogs/add-book.html", slug=book.slug))


@app.route("/my_books", methods=["POST", "GET"])
@login_required(required=True)
def my_books():
    books = Books.query.all()
    return render_template("blogs/my-books.html", books=books)


@app.route("/top_books", methods=["POST", "GET"])
@login_required(required=True)
def top_books():
    books = Books.query.order_by(Books.page_count)
    return render_template("blogs/top-books.html", books=books)


@app.route("/log_out")
@login_required(required=True)
def log_out():
    session.pop("user_id")
    username = session.pop("username")
    flash(f"{username} user successfully loged out", "info")
    return redirect(url_for("home"))


@app.route("/profile_info", methods=["POST", "GET"])
@login_required(required=True)
def profile_info():
    user = User.query.filter_by(id=session.get('user_id')).first()
    return render_template('blogs/profile.html', user=user)