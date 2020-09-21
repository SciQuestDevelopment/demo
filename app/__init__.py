from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__, static_folder='../static',template_folder='../templates')
app.config.from_object('config')
db = SQLAlchemy(app)

from app.view import api
app.register_blueprint(api)


# Build the database if db does not exist
if not os.path.exists('app.db'):
    db.create_all()

posts = [
    {
        'author': 'Corey Schafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2018'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'用户{form.username.data}注册成功!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('登陆成功', 'success')
            return redirect(url_for('home'))
        else:
            flash('登陆失败 请检查用户名和密码', 'danger')
    return render_template('login.html', title='Login', form=form)