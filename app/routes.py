import pandas as pd
from flask import render_template, request, make_response, redirect, url_for
from app import app, badgecraft


# TOKEN = "f30e9f7e-5f76-4119-8974-8a1b2ea164e3"


# base application route
@app.route('/login')
@app.route('/')
def index():
    return render_template('login.html', protected=True)


# overview route
@app.route('/overview')
def overview():
    # instantiate needed var for overview page
    loggedInUser = request.cookies.get("username")
    studentCount = badgecraft.FETCHED_DATA["list.projects.list.users.list.name"].unique()
    studentList = badgecraft.FETCHED_DATA["list.projects.list.users.list.name"].unique()
    projectList = badgecraft.FETCHED_DATA["list.projects.list.name"].unique()

    projectInfo = {"projectName": projectList, "projectStatus": badgecraft.projectDetails}
    projectInfoDf = pd.DataFrame(data=projectInfo)

    totalBadgeCount = 0
    belowAverageCount = 0

    # calculate average badge count per student
    for student in studentList:
        badgecount = badgecraft.getbadgecount(badgecraft.FETCHED_DATA, student)
        if badgecount < 12:
            belowAverageCount = belowAverageCount + 1
        totalBadgeCount += badgecount

    averageBadgeCount = round(totalBadgeCount / len(studentCount))

    # projectInfoDf.head()

    # render templates with vars
    return render_template('overview.html', fetch_amount=badgecraft.fetched_amount, protected=False,
                           student_count=len(studentCount),
                           current_user=loggedInUser, number_badges=round(totalBadgeCount), project_info=projectInfoDf,
                           average_badgecount=averageBadgeCount, below_average_count=belowAverageCount)


# helppage route
@app.route('/helppage')
def helppage():
    loggedInUser = request.cookies.get("username")
    return render_template('helppage.html', protected=False, current_user=loggedInUser)


# Detail rout
@app.route('/detail/<name>')
def detail(name):
    studentData = badgecraft.getStudentProgress(badgecraft.FETCHED_DATA, name)
    loggedInUser = request.cookies.get("username")

    return render_template('detail.html', protected=False, current_user=loggedInUser, student_data=studentData,
                           student=name)


# students route
@app.route('/students')
def users():
    studentNames = badgecraft.FETCHED_DATA["list.projects.list.users.list.name"].unique()
    tempdf = badgecraft.FETCHED_DATA.drop_duplicates(subset=['list.projects.list.users.list.name'])
    tempdf['list.projects.list.users.list.email'].replace(r'^\s*$', "Empty", regex=True)
    studentEmails = tempdf["list.projects.list.users.list.email"]
    data = {'student.name': studentNames, 'student.email': studentEmails,
            'project.details': badgecraft.StudentPageOverview}
    completeStudentInfoList = pd.DataFrame(data=data)

    loggedInUser = request.cookies.get("username")

    sort = request.args.get("sort")
    if sort == "name-asc":
        studentList = completeStudentInfoList.sort_values(by='student.name', ascending=True)

    elif sort == "name-desc":
        studentList = completeStudentInfoList.sort_values(by='student.name', ascending=False)

    # elif sort == "badge-asc":
    #     studentList = completeStudentInfoList.sort_values(by='project.details'[0], ascending=True)

    # elif sort == "badge-desc":
    #     studentList = completeStudentInfoList.sort_values(by='project.details'[0], ascending=False)

    # elif sort == "quest-asc":
    #     studentList = completeStudentInfoList.sort_values(by='project.details'[1], ascending=True)

    # elif sort == "quest-desc":
    #     studentList = completeStudentInfoList.sort_values(by='project.details'[1], ascending=False)

    # elif sort == "qual-asc":
    #     studentList = completeStudentInfoList.sort_values(by='project.details'[2], ascending=True)

    # elif sort == "qual-desc":
    #     studentList = completeStudentInfoList.sort_values(by='project.details'[2],  ascending=False)
    else:
        # if `sort` is none of the above, default to showing raw list
        studentList = completeStudentInfoList

    return render_template('students.html', protected=False, students=studentList, current_user=loggedInUser)


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
    return render_template('classes.html', classes=classes, labels=labels, today=today, total=total, protected=False,
                           current_user=loggedInUser)


@app.route('/account', methods=['POST'])
def account():
    username = request.form['username']
    password = request.form['password']

    res = badgecraft.login(username, password)
    print(res)
    if res["success"]:
        token = res["token"]
        userid = badgecraft.getId({"a": token})
        username = badgecraft.getUsername({"a": token})

        # redirect after login
        resp = make_response(redirect(url_for("overview")))
        # set cookies with current user info
        resp.set_cookie('username', username)
        resp.set_cookie('token', token)
        resp.set_cookie("userId", userid)

        return resp

    else:
        return """{"response":400}"""
