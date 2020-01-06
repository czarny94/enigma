from wtforms import Form, StringField, PasswordField, BooleanField, validators

class LoginForm(Form):
    username = StringField("Username")
    password = PasswordField("Password")
