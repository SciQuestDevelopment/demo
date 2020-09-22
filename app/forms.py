from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    university = StringField('学校',
                           validators=[DataRequired(), Length(min=2, max=20)])
    major = StringField('专业',
                             validators=[DataRequired(), Length(min=2, max=20)])
    interest1 = StringField('兴趣 1',
                        validators=[DataRequired(), Length(min=2, max=20)])
    interest2 = StringField('兴趣 2',
                        validators=[Length(min=2, max=20)])
    confirm_password = PasswordField('确认密码',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('登陆')