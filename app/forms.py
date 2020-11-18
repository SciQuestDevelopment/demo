from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms.widgets.core import ListWidget,CheckboxInput
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField,SelectField, SelectMultipleField
from flask_wtf.html5 import URLField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,url
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
            raise ValidationError('用户名已存在')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('邮箱地址已存在，请更换邮箱')


class LoginForm(FlaskForm):
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember = BooleanField('记住我')
    submit = SubmitField('登陆')


class UpdateAccountForm(FlaskForm):
    username = StringField('用户名',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('邮箱',
                        validators=[DataRequired(), Email()])
    picture = FileField('更新头像', validators=[FileAllowed(['jpg', 'png'])])
    university = StringField('学校',
                             validators=[DataRequired(), Length(min=2, max=20)])
    major = StringField('专业',
                        validators=[DataRequired(), Length(min=2, max=20)])
    interest1 = StringField('兴趣 1',
                            validators=[DataRequired(), Length(min=2, max=20)])
    interest2 = StringField('兴趣 2',
                            validators=[Length(min=2, max=20)])

    submit = SubmitField('更新')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('用户名已存在，请更换用户名')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('邮箱已存在，请更换邮箱')


class PostForm(FlaskForm):
    title = StringField('标题', validators=[DataRequired()])
    description = TextAreaField('主题', validators=[DataRequired()])
    url = URLField(validators=[url()])
    venue = StringField('期刊', validators=[DataRequired()])
    submit = SubmitField('确认发布')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('该邮箱尚未注册')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


# class ExampleForm(FlaskForm):
#     choices = MultiCheckboxField('Routes', coerce=int)
#     submit = SubmitField("Set User Choices")

class PubQueryForm(FlaskForm):
    pub_name = StringField('文献名称', validators=[DataRequired()])
    venue_name = MultiCheckboxField('期刊名称', choices=[('', 'All Sources'), (
    '&quot;advanced science&quot; source:advanced source:science', 'Advanced Science'), (
                                              '&quot;advanced materials&quot; source:advanced source:materials',
                                              'Advanced Materials'),
                                              (
                                              '&quot;progress in materials science&quot; source:progress source:in source:materials source:science',
                                              'Progress in materials science'),
                                              ('&quot;joule&quot; source:joule', 'Joule'),
                                              ('&quot;science&quot; source:science', 'Science'), (
                                              '&quot;nature reviews materials&quot; source:nature source:reviews source:materials',
                                              'Nature Reviews Materials'),
                                              (
                                              '&quot;nature reviews chemistry&quot; source:nature source:reviews source:chemistry',
                                              'Nature Reviews Chemistry'), (
                                              '&quot;nature chemistry&quot; source:nature source:chemistry',
                                              'Nature Chemistry'),
                                              (
                                              '&quot;chemical society reviews&quot; source:chemical source:society source:reviews',
                                              'Chemical Society Reviews')])

    submit = SubmitField('搜索')


class VenueQueryForm(FlaskForm):
    pub_name = StringField('文献名称', validators=[DataRequired()])
    venue_name = SelectField('期刊名称', choices=[('', 'All Sources'),('&quot;advanced science&quot; source:advanced source:science', 'Advanced Science'),('&quot;advanced materials&quot; source:advanced source:materials','Advanced Materials'),
                                              ('&quot;progress in materials science&quot; source:progress source:in source:materials source:science','Progress in materials science'),('&quot;joule&quot; source:joule','Joule'),
                                              ('&quot;science&quot; source:science','Science'),('&quot;nature reviews materials&quot; source:nature source:reviews source:materials','Nature Reviews Materials'),
                                              ('&quot;nature reviews chemistry&quot; source:nature source:reviews source:chemistry','Nature Reviews Chemistry'),('&quot;nature chemistry&quot; source:nature source:chemistry','Nature Chemistry'),
                                              ('&quot;chemical society reviews&quot; source:chemical source:society source:reviews','Chemical Society Reviews')])

    submit = SubmitField('搜索')


class AuthorQueryForm(FlaskForm):
    author_name = StringField('作者', validators=[DataRequired()])
    submit = SubmitField('搜索')
