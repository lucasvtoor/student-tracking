from flask import render_template
from app import app


# base application route
@app.route('/')
def index():
    return render_template('index.html')

# overview route
@app.route('/overview')
def overview():
    return render_template('overview.html')

# user route
@app.route('/user')
def user():
    return render_template('users.html')


