from flask import Flask, render_template
from app import app

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Dasraf'}
    return '''
<html>
    <head>
        <title>User Page</title>
    </head>
    <body>
        <h1>Hello, ''' + user['username'] + '''!</h1>
    </body>
</html>'''
@app.route('/users')
def users():
    return render_template('users.html')