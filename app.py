from datetime import datetime
from flask import Flask, render_template, url_for, request, redirect, flash

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html', title='Gym Finder')


@app.route('/find', methods=["GET", "POST"])
def find_gyms():
    if request.method == 'POST':
        location = request.form["location"]
        return "Searching for gyms around " + location

if __name__ == "__main__":
    app.run(debug=True)
