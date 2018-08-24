from flask import render_template, url_for, flash, redirect, request
from crm import app, db, bcrypt
from crm.models import User, Company, Products, Feedback
from crm.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, login_required, logout_user


posts = [
    {
        'author': 'Aman Gupta',
        'title': 'Firefox',
        'content': 'Eggcellent',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Abhijeeth V Madalgi',
        'title': 'Chrome',
        'content': 'Good RAM Usage',
        'date_posted': 'April 21, 2018'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        if form.types.data == 'Cust':
            user = User(username=form.username.data, email=form.email.data, password=hash_pw)
        else:
            user = Company(username=form.username.data, email=form.email.data, password=hash_pw)

        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.types.data == 'Cust':
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
        else:
            comp = Company.query.filter_by(email=form.email.data).first()
            if comp and bcrypt.check_password_hash(comp.password, form.password.data):
                login_user(comp, form.remember.data)
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
