from flask import Flask, render_template, request, url_for, redirect, flash
from forms import forms
from os import urandom

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
            flash('formularz wypełniony poprawnie')
            return redirect(url_for('register'))
        else:
            flash('dupa')
            return redirect(url_for('mainpage'))
    return render_template('register.html', register_active=True, form=form)

@app.route('/profil', methods=["POST", "GET"])
def profil():
    return render_template('profil.html', profil_active=True)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()