from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import EqualTo, Length, Email, DataRequired, ValidationError
from market.models import User


class SignupForm(FlaskForm):
    # when a func starts with validate followed by underscore and name
    # flask auomatically runs that function and checks if a field followed
    # by the underscore exists or not. if it does then it does the validation
    def validate_user(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("User already exists!")
        
    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError("User with the email already exists!")

    username = StringField(label="Username", validators=[Length(min=3, max=12), DataRequired()] )
    email = StringField(label="Email", validators=[Email(), DataRequired()])
    password = PasswordField(label="Password", validators=[Length(min=8, max=16), DataRequired()])
    confirm_password = PasswordField(label="Confirm password", validators=[EqualTo('password'), DataRequired()])
    submit = SubmitField(label="submit")

class LoginForm(FlaskForm):
    username = StringField(label="Username", validators=[DataRequired()] )
    password = PasswordField(label="Password", validators=[DataRequired()])
    submit = SubmitField(label="submit")

class PurchaseForm(FlaskForm):
    submit = SubmitField(label="Buy")