from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField
from wtforms.fields.html5 import EmailField
from wtforms import validators

class LoginForm(FlaskForm):
    username = StringField("Nazwa Użytkownika", validators=[validators.DataRequired()])
    password = PasswordField("Hasło", validators=[validators.DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField("Nazwa Użytkownika", validators=[validators.DataRequired(), validators.Length(min=4, max=25)])
    email = EmailField('Adres Email', [validators.DataRequired(), validators.Email()])
    password = PasswordField('Hasło', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Hasła musza być takie same')
    ])
    confirm = PasswordField('Powtórz hasło')
    recaptcha = RecaptchaField()
