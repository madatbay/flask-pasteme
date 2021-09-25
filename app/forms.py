from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from app.models import User

class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    password_confirm = PasswordField(validators=[InputRequired(), Length(min=6, max=20), EqualTo("password")], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Sign up")

    def validate_username(self, username):
        db_user = User.query.filter_by(username=username.data).first()
        if db_user:
            raise ValidationError("User with this username already exits")

class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=6, max=20)],
        render_kw={"placeholder": "Username"},
    )
    password = PasswordField(validators=[InputRequired(), Length(min=6, max=20)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Sign in")


class SnippetForm(FlaskForm):
    title = StringField(validators=[InputRequired(), Length(min=0, max=40)], render_kw={"placeholder": "Title"})
    body = TextAreaField(validators=[InputRequired(), Length(min=0, max=600)], render_kw={"placeholder": "Snippet"})
    submit = SubmitField("Paste")
