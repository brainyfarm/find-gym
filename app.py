from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html', title='Gym Finder')


@app.route('/findgym', methods=["POST"])
def find_gym():
    return 'Find the fucking gym'    

if __name__ == "__main__":
    app.run(debug=True)
