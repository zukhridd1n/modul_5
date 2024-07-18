from flask_wtf import FlaskForm
from sqlalchemy.testing.pickleable import User
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login", validators=[DataRequired()])


class RegistrationForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=20)])
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField("Email", validators=[DataRequired(), ])
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register", validators=[DataRequired()])


class DeleteBook(FlaskForm):
    book_id = StringField("Book ID", validators=[DataRequired()])
    submit = SubmitField("Delete Book", validators=[DataRequired()])


class DeleteAccountForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=2, max=20)])
    email = EmailField("Email", validators=[DataRequired(), ])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Delete Account", validators=[DataRequired()])

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError("Username not found.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("Email not found.")


class AddBookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    page_count = StringField("Page Counts", validators=[DataRequired()])
    submit = SubmitField("Add Book", validators=[DataRequired()])