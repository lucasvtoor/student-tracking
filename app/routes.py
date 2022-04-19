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

# help route
@app.route('/help')
def helppage():
    return render_template('helppage.html')

