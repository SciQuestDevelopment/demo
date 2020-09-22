from datetime import datetime
from flask_login import UserMixin
from app import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg');
    university = db.Column(db.String(60), nullable=False)
    major = db.Column(db.String(60), nullable=False)
    interest1 = db.Column(db.String(60), nullable=False)
    interest2 = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)


    def __repr__(self):
        return '<User {} {}>'.format(self.email, self.id)



class Post(db.Model):
    id = db.Column(db.Integer, index=True, unique=True, primary_key=True, autoincrement=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return '<Post {} {} {} {}>'.format(self.title, self.date_posted, self.description, self.content)
