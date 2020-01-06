from flask import Flask, render_template, request, url_for, redirect
from forms import forms
from os import urandom

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')
SECRET_KEY = urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

@app.route('/', methods=["GET", "POST"])
def mainpage():
    return render_template('mainpage.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('profil'))
    return render_template('login.html', form=form)

@app.route('/profil', methods=["POST", "GET"])
def profil():
    return render_template('profil.html')

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()