from market import app, db
from flask import render_template, redirect, url_for, flash
from market.models import Item, User
from market.forms import SignupForm, LoginForm, PurchaseForm
from market import bcrypt

from flask_login import login_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/market", methods=["GET", "POST"])
@login_required
def market_page():
    purchaseForm = PurchaseForm()
    if purchaseForm.validate_on_submit():
        print(purchaseForm)

    items = Item.query.all()
    return render_template("market.html", items=items, form=purchaseForm)

@app.route("/signup", methods=['GET', 'POST'])
def signup_page():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("market_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(err_msg[0], category="danger")

    return render_template("signup.html", form=form)

@app.route("/login", methods=["GET","POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.verify_password(f"{form.password.data}"):
            login_user(user)
            flash(f"{user.username} logged in!", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Username and password do not match!")

    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET", "POST"])
def logout():
    logout_user()
    flash("Logout successfull!", category="success")
    return redirect(url_for("home"))