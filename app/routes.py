from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt, mail
from app.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                       PostForm, RequestResetForm, ResetPasswordForm,
                       PubQueryForm,AuthorQueryForm,VenueQueryForm)
from app.models import User, Post
from PIL import Image
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from scholarly import scholarly

import os
import secrets
import html


@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)
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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password,
                    university=form.university.data, major=form.major.data, interest1=form.interest1.data,
                    interest2=form.interest2.data)

        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('登陆成功', 'success')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('登陆失败，请检查你的用户名和密码', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.university = form.university.data
        current_user.major = form.major.data
        current_user.interest1 = form.interest1.data
        current_user.interest2 = form.interest2.data
        db.session.commit()
        flash('账户更新成功！', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.university.data = current_user.university
        form.major.data = current_user.major
        form.interest1.data = current_user.interest1
        form.interest2.data = current_user.interest2
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='账户信息',
                           image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, description=form.description.data, author=current_user,
                    url=form.url.data, venue=form.venue.data)
        db.session.add(post)
        db.session.commit()
        flash('发表成功！', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='发表文章',
                           form=form, legend='发表文章')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.description = form.description.data
        post.url = form.url.data
        post.venue = form.venue.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.description.data = post.description
        form.url.data = post.url
        form.venue.data = post.venue
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user) \
        .order_by(Post.date_posted.desc()) \
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@SciquestServer.com',
                  recipients=[user.email])
    msg.body = f'''访问以下链接，以重置您的密码:
{url_for('reset_token', token=token, _external=True)}

如果不是本人操作，请忽略此邮件
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('重置邮件已发送至您的邮箱，请查收', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('密钥过期或失效', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('重置密码成功', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='重置密码', form=form)


@app.route("/search_pub", methods=['GET', 'POST'])
def pub_query():
    form = PubQueryForm()
    if form.validate_on_submit():
        search_query = scholarly.search_pubs(form.pub_name.data)
        pubs = []
        for i in range(20):
            try:
                pub = next(search_query)
                pubs.append(pub)
            except:
                # print("End of the iterator")
                break;
        return render_template('pub_results.html', title='文献查询结果', pubs=pubs)
    return render_template('search_pub.html', title='文献查询', form=form)


@app.route("/search_author", methods=['GET', 'POST'])
def auth_query():
    form = AuthorQueryForm()
    if form.validate_on_submit():
        search_query = scholarly.search_author(form.author_name.data)
        authors = []
        for i in range(20):
            try:
                author = next(search_query)
                authors.append(author)
            except:
                # print("End of the iterator")
                break;
        return render_template('author_results.html', title='文献查询结果', authors=authors)
    return render_template('search_author.html', title='查作者', form=form)

@app.route("/search_venue", methods=['GET', 'POST'])
def venue_query():
    form = VenueQueryForm()
    if form.validate_on_submit():
        query = form.pub_name.data + form.venue_name.data
        query = html.unescape(query)
        print(query)
        search_query = scholarly.search_pubs(query)
        pubs = []
        for i in range(20):
            try:
                pub = next(search_query)
                pubs.append(pub)
            except:
                # print("End of the iterator")
                break;
        return render_template('pub_results.html', title='文献查询结果', pubs=pubs)
    return render_template('search_venue.html', title='查文献', form=form)

