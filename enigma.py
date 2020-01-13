from os import urandom

from flask import Flask, render_template, request, url_for, redirect, flash, abort
from flask_login import LoginManager, UserMixin, login_required, login_user

from forms import forms
from sql import enigma_cockroachdb

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

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)

# połączenie z bazą danych
cockroach = enigma_cockroachdb.Cockroach()


class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = str(id).encode('UTF-8').decode('UTF-8')
        self.username = username
        self.email = email

    # def is_authenticated(self):
    #     return True
    #
    # # TODO: zaimplementować mechanizm zaminy statusu użytkowników - aktywny/nieaktywny
    # def is_active(self):
    #     return True
    #
    # # TODO: zaimplementować możliwość użytkowników anonimowych
    # def is_anonymous(self):
    #     return False
    #
    # def get_id(self):
    #     return self.id

    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.username, self.email)


@app.route('/', methods=["GET", "POST"])
def mainpage():
    return render_template('mainpage.html', mainpage_active=True)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user_data = cockroach.check_password(form.username.data,form.password.data)
        if user_data:
            user = User(user_data[0], user_data[1], user_data[2])
            login_user(user)
            flash('Zalogowano się pomyślnie')
            next = request.args.get('next')
            # if not is_safe_url(next):
            #     return abort(400)
            return redirect(next or url_for('profil'))
    return render_template('login.html', login_active=True, form=form)


@app.route('/register', methods=["POST", "GET"])
def register():
    form = forms.RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            cockroach.create_account(username=form.username.data, password=form.password.data, email=form.email.data)
            flash('Konto utworzone, witamy w systemie enigma {}'.format(form.username.data))
            return redirect(url_for('profil'))
        else:
            flash('prosze poprawnie uzupełnić formularz')
            return redirect(url_for('register'))
    return render_template('register.html', register_active=True, form=form)


@app.route('/profil', methods=["POST", "GET"])
@login_required
def profil():
    return render_template('profil.html', profil_active=True)


@login_manager.user_loader
def load_user(user_id):
    return User.get_id(user_id)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
