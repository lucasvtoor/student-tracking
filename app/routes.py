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

# classes route
@app.route('/classes')
def classes():
    classes = [
        {
            'name':'Klas 1A',
            'members':'20'
        },
        {
            'name':'Klas 2A',
            'members':'16'
        },
        {
            'name':'Klas 3A',
            'members':'22'
        },
        {
            'name':'Klas 4A',
            'members':'18'
        },
        {
            'name':'Klas 5A',
            'members':'5'
        },
    ]
    return render_template('classes.html', classes = classes)    