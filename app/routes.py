import pandas as pd
from flask import render_template, request, make_response, redirect, url_for
from app import app, fetchData
from app.static.py.badgecraft import fetch, getId, login, getFetchedData, getUsername, projectDetails, getbadgecount


# TOKEN = "f30e9f7e-5f76-4119-8974-8a1b2ea164e3"
# FETCHED_DATA = fetch(TOKEN)



# base application route
@app.route('/login')
@app.route('/')
def index():
    return render_template('login.html', protected=True)


# overview route
@app.route('/overview')


def overview():
    loggedInUser = request.cookies.get("username")
    studentCount = fetchData["list.projects.list.users.list.name"].nunique()
    studentList = fetchData["list.projects.list.users.list.name"].unique()
    projectList = fetchData["list.projects.list.name"].unique()

    projectInfo = {"projectName": projectList, "projectStatus": projectDetails}
    projectInfoDf = pd.DataFrame(data=projectInfo) 


    totalBadgeCount = 0
    belowAverageCount = 0

    for student in studentList:
        badgecount = getbadgecount(fetchData, student)
        if(badgecount < 12):
            belowAverageCount+1
        totalBadgeCount += badgecount

    averageBadgeCount = round(totalBadgeCount/ studentCount)

    projectInfoDf.head()

    return render_template('overview.html', protected=False, student_count = studentCount, 
    current_user = loggedInUser, number_badges = totalBadgeCount, project_info = projectInfoDf,
    average_badgecount = averageBadgeCount, below_average_count = belowAverageCount)


# helppage route
@app.route('/helppage')
def helppage():
    loggedInUser = request.cookies.get("username")
    return render_template('helppage.html', protected=False, current_user = loggedInUser)


# students route
@app.route('/students')
def users():
    loggedInUser = request.cookies.get("username")
    students = [
        {
            'name': 'Mike Schilder',
            'email': 'mike.schilder@hva.nl',
            'logIn': '14/april/2022',
            'badges': '5',
            'quests': '5',
            'certificates': '5'
        },
        {
            'name': 'Hooshang Kooshani',
            'email': 'hooshang.kooshani@hva.nl',
            'logIn': '14/april/2022',
            'badges': '5',
            'quests': '5',
            'certificates': '5'
        },
        {
            'name': 'Farzad Mobasher',
            'email': 'farzad.mobasher@hva.nl',
            'logIn': '14/april/2022',
            'badges': '5',
            'quests': '5',
            'certificates': '5'
        },
        {
            'name': 'Ayoub Barkani',
            'email': 'ayoub.barkani@hva.nl',
            'logIn': '14/april/2022',
            'badges': '5',
            'quests': '5',
            'certificates': '5'
        },
        {
            'name': 'Po Man',
            'email': 'po.man@hva.nl',
            'logIn': '14/april/2022',
            'badges': '5',
            'quests': '5',
            'certificates': '5'
        }

    ]
    return render_template('students.html', protected=False, students=students, current_user = loggedInUser)



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

    loggedInUser = request.cookies.get("username")
    return render_template('classes.html', classes=classes, labels=labels, today=today, total=total, protected=False, current_user = loggedInUser)


@app.route('/account', methods=['POST'])
def account():
    username = request.form['username']
    password = request.form['password']

    res = login(username, password)
    print(res)
    if res["success"]:
        token = res["token"]
        id = getId({"a":token})
        username = getUsername({"a":token})


        resp = make_response(redirect(url_for("overview")))
        resp.set_cookie('username', username)
        resp.set_cookie('token', token)
        resp.set_cookie("userId", id)

        return resp

    else:
        return """{"response":400}"""


