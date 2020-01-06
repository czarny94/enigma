from flask import Flask, render_template, redirect, url_for, request
from jinja2 import Template, Environment, FileSystemLoader

app = Flask(__name__,
            static_folder='static',
            static_url_path='/static',
            template_folder='templates')
# file_loader = FileSystemLoader('templates')
# env = Environment(loader=file_loader)

@app.route('/', methods=["GET", "POST"])
@app.route('/login', methods=["POST", "GET"])
def login():
    return render_template('mainpage.html')
    # return env.get_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)