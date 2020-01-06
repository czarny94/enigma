from flask import Flask, render_template, redirect, url_for, request
import forms

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')
# file_loader = FileSystemLoader('templates')
# env = Environment(loader=file_loader)

@app.route('/', methods=["GET", "POST"])
def mainpage():
    return render_template('mainpage.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    # form = forms.LoginForm(request.form)
    # user = form.username.data
    # password = form.username.password
    return render_template('login.html')
    # return env.get_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)