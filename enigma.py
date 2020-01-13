from flask import Flask, render_template, request, url_for, redirect, flash
from forms import forms
from os import urandom
from sql import enigma_cockroachdb
from flask_login import LoginManager, login_manager, UserMixin

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')
# utworzenie losowego klucza prywatnego dla ochrony przed CSRF
SECRET_KEY = urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LcS8MwUAAAAAHx02QRjhBWh76MGRY6E2KKS9NEM"
app.testing = True

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.email)

@app.route('/', methods=["GET", "POST"])
def mainpage():
    return render_template('mainpage.html', mainpage_active=True)

@app.route('/login', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('profil'))
    return render_template('login.html', login_active=True, form=form)

@app.route('/register', methods=["POST", "GET"])
def register():
    form = forms.RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            cockroach = enigma_cockroachdb.Cockroach()
            cockroach.create_account(username=form.username.data, password=form.password.data, email=form.email.data)
            flash('Konto utworzone, witamy w systemie enigma {}'.format(form.username.data))
            return redirect(url_for('profil'))
        else:
            flash('prosze poprawnie uzupełnić formularz')
            return redirect(url_for('register'))
    return render_template('register.html', register_active=True, form=form)

@app.route('/profil', methods=["POST", "GET"])
def profil():
    return render_template('profil.html', profil_active=True)

# @login_manager.user_loader
# def load_user(user_id):
#     return User.get(user_id)

def main():
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.run(debug=True)

if __name__ == '__main__':
    main()