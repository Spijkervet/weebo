from flask_wtf import FlaskForm
from wtforms.fields import StringField, BooleanField, SubmitField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    email = StringField("Name", validators=[Required()], render_kw={"type": "email", "placeholder": "Email"})
    password = StringField("Password", validators=[Required()], render_kw={"type": "password", "placeholder": "Password"})
    remember = BooleanField("Remember", render_kw={"class": "form-check-input"})
    submit = SubmitField("Login")
