from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField("użytkownik", validators=[DataRequired()])
    password = PasswordField("hasło", validators=[DataRequired()])
