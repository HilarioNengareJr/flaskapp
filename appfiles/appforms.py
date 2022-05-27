from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms.fields import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .appmodels import User
from flask_login import current_user


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[
        DataRequired(),
        Length(min=2, max=20)
    ])
    email = StringField(label='Email Address', validators=[DataRequired(),
                                                           Length(min=6, max=35)])
    password = PasswordField(label='Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField(label='Confirm Password', validators=[
        DataRequired(),
        EqualTo('password')
    ])
    submit = SubmitField(label='Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is already take.")


class LoginForm(FlaskForm):
    email = StringField(label='Email Address', validators=[DataRequired(),
                                                           Length(min=6, max=35)])
    password = PasswordField(label='Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    remember = BooleanField(label='Remember me')
    submit = SubmitField(label='Login')


class PostForm(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired()])
    media = FileField(label='Upload Images', validators=[FileAllowed(('jpeg', 'jpg', 'png'))])
    content = TextAreaField(label='Description', validators=[DataRequired()])
    submit = SubmitField(label='Post')


class CommentPostForm(FlaskForm):
    content = TextAreaField(label='Comment')
    submit = SubmitField(label='Post')
