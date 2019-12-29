from flask import Flask, render_template
from flask_login import

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('mainpage.html')

if __name__ == '__main__':
    app.run(debug=True)