from os import urandom

from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, login_required, login_user, logout_user

from forms import forms
from sql import enigma_cockroachdb
import json

app = Flask(__name__, )
# utworzenie losowego klucza prywatnego dla ochrony przed CSRF
SECRET_KEY = urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
# app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = "6LcS8MwUAAAAAHx02QRjhBWh76MGRY6E2KKS9NEM"
app.testing = True

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"

# połączenie z bazą danych
cockroach = enigma_cockroachdb.Cockroach()


@app.route('/', methods=["GET", "POST"])
def mainpage():
    return render_template('mainpage.html', mainpage_active=True)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        account = enigma_cockroachdb.Account(cockroach)
        user_data = account.check_password(form.username.data, form.password.data)
        if user_data:
            account.id = user_data[0]
            account.username = user_data[1]
            account.email = user_data[2]
            login_user(account)
            flash('Zalogowano się pomyślnie')
            # next = request.args.get('next')
            # if not is_safe_url(next):
            #     return abort(400)
            return redirect(url_for('profil'))
        flash('niepoprawny login lub hasło')
        return redirect(url_for('login'))
    return render_template('login.html', login_active=True, form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = forms.RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            account = enigma_cockroachdb.Account(cockroach)
            is_created = account.create_account(username=form.username.data, password=form.password.data,
                                                email=form.email.data)
            if is_created:
                flash('Konto utworzone, możesz się teraz zalogować')
                return redirect(url_for('login'))
            else:
                flash('Konto nie zostało utworzone, prawdopodobnie taki użytkownik już istnieje')
                return redirect(url_for('register'))
        else:
            flash('prosze poprawnie uzupełnić formularz')
            return redirect(url_for('register'))
    return render_template('register.html', register_active=True, form=form)


@app.route('/profil')
@login_required
def profil():
    return render_template('profil.html', profil_active=True)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('zostaleś wylogowany')
    return redirect(url_for('mainpage'))


@login_manager.user_loader
def load_user(id):
    if id is not None:
        return cockroach.session.query(enigma_cockroachdb.Account).get(id)
    return None

@app.route('/generate_keys', methods=["POST", "GET"])
@login_required
def generate_keys():
    return render_template('generate_keys.html')

@app.route('/get_keys', methods=["GET", "POST"])
# @login_required
def get_keys():
    if request.method == "POST":
        data = json.loads(request.get_data().decode())
        print(type(data))
        user_id = data['key']['key']['users'][0]['userId']['name']
        privateKeyArmored = data['key']['privateKeyArmored']
        publicKeyArmored = data['key']['publicKeyArmored']
        revocationCertificate = data['key']['revocationCertificate']
    # return render_template('get_keys')


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
