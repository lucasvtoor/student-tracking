from crypt import methods
from flask import render_template, request, make_response, redirect, url_for
from app import app
from app.static.py.badgecraft import fetch, getId, login, getFetchedData


TOKEN = "f30e9f7e-5f76-4119-8974-8a1b2ea164e3"
FETCHED_DATA = fetch(TOKEN)


# base application route
@app.route('/login')
@app.route('/')
def index():
    return render_template('login.html', protected=True)


# overview route
@app.route('/overview')
def overview():
    return render_template('overview.html', protected=False)


# helppage route
@app.route('/helppage')
def helppage():
    return render_template('helppage.html', protected=False)


# user route
@app.route('/users')
def users():
    return render_template('users.html', protected=False)


# classes route
@app.route('/classes')
def classes():
    classes = [
        {
            'name': 'Klas 1A',
            'members': '20'
        },
        {
            'name': 'Klas 2A',
            'members': '16'
        },
        {
            'name': 'Klas 3A',
            'members': '22'
        },
        {
            'name': 'Klas 4A',
            'members': '18'
        },
        {
            'name': 'Klas 5A',
            'members': '5'
        },
    ]

    data = [
        ("Klas 1A", 15, 45),
        ("Klas 2A", 10, 43),
        ("Klas 3A", 12, 36),
        ("Klas 4A", 7, 40),
        ("Klas 5A", 19, 65),
    ]

    labels = [row[0] for row in data]
    today = [row[1] for row in data]
    total = [row[2] for row in data]

    return render_template('classes.html', classes=classes, labels=labels, today=today, total=total, protected=False)


@app.route('/account', methods=['POST'])
def account():
    username = request.form['username']
    password = request.form['password']

    res = login(username, password)
    print(res)
    if res["success"]:
        token = res["token"]
        id = getId({"a":token})

        print("FETCHED DATA: ", FETCHED_DATA.info())

        resp = make_response(
            redirect(url_for("overview", user_amount=FETCHED_DATA["list.projects.list.users.list.name"].nunique))
            # render_template('overview.html', user_amount=FETCHED_DATA["list.projects.list.users.list.name"].nunique)
            
            )
        resp.set_cookie('token', token)
        resp.set_cookie("userId", id)

        return resp

    else:
        return """{"response":400}"""

