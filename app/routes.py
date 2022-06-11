import pandas as pd
from flask import render_template, request, make_response, redirect, url_for, Response
from app import app, badgecraft
from flask_paginate import Pagination,get_page_args


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

    # search projects
    searchTerm = request.args.get("searchTerm")
    if(searchTerm != None):
        sortingList = projectInfoDf[projectInfoDf['projectName'].str.contains(searchTerm, case=False, na=False)]
    else:
        sortingList = projectInfoDf

    # render templates with vars
    return render_template('overview.html', fetch_amount=badgecraft.fetched_amount, protected=False,
                           student_count=len(studentCount),
                           current_user=loggedInUser, number_badges=round(totalBadgeCount), project_info=sortingList,
                           average_badgecount=averageBadgeCount, below_average_count=belowAverageCount)


# helppage route
@app.route('/helppage')
def helppage():
    loggedInUser = request.cookies.get("username")
    return render_template('helppage.html', protected=False, current_user=loggedInUser)





studentList = badgecraft.FETCHED_DATA["list.projects.list.users.list.name"].unique()
infoArray = []
for student in studentList:
    infoArray.append(badgecraft.getstudentProjectCounts(badgecraft.FETCHED_DATA, student))

studentInfo = pd.DataFrame(data=infoArray)

# Detail rout
@app.route('/detail/<name>')
def detail(name):
    studentData = badgecraft.getStudentProgress(badgecraft.FETCHED_DATA, name)
    loggedInUser = request.cookies.get("username")


    return render_template('detail.html', protected=False, current_user=loggedInUser, student_data=studentData, name=name)


def get_users(offset=0,per_page=20,df=studentInfo):
    return df[offset: offset+per_page]


# students route
@app.route('/students')
def users():
    
    loggedInUser = request.cookies.get("username")

    sort = request.args.get("sort")
    if sort == "name-asc":
        sortingList = studentInfo.sort_values(by='student.name', ascending=True)

    elif sort == "name-desc":
        sortingList = studentInfo.sort_values(by='student.name', ascending=False)

    elif sort == "badge-asc":
        sortingList = studentInfo.sort_values(by='student.badge', ascending=True)

    elif sort == "badge-desc":
        sortingList = studentInfo.sort_values(by='student.badge', ascending=False)

    elif sort == "quest-asc":
        sortingList = studentInfo.sort_values(by='student.quest', ascending=True)

    elif sort == "quest-desc":
        sortingList = studentInfo.sort_values(by='student.quest', ascending=False)

    elif sort == "cert-asc":
        sortingList = studentInfo.sort_values(by='student.certificate', ascending=True)

    elif sort == "cert-desc":
        sortingList = studentInfo.sort_values(by='student.certificate',  ascending=False)
    else:
        # if `sort` is none of the above, default to showing raw list
        sortingList = studentInfo

    # search students
    searchTerm = request.args.get("searchTerm")
    if(searchTerm != None):
        sortingList = studentInfo[studentInfo['student.name'].str.contains(searchTerm, case=False, na=False)]

    page,per_page,offset = get_page_args(page_parameter="page",per_page_parameter="per_page")

    total = len(studentInfo)

    pagination_users = get_users(offset=offset,per_page=per_page, df=sortingList)

    pagination = Pagination(page=page,per_page=per_page,total=total, css_framework='bootstrap5')

    return render_template('students.html', protected=False, current_user=loggedInUser, students=pagination_users,page=page,per_page=per_page,pagination=pagination)


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

@app.route('/download_student_csv')
def get_csv():
    downloadable_csv = badgecraft.FETCHED_DATA.to_csv(index=False)
    return Response(
        downloadable_csv,
        mimetype="text/csv",
        headers={"Content-disposition":
                 "attachment; filename=dataStudents.csv"})


@app.route('/account', methods=['POST'])
def account():
    username = request.form['username']
    password = request.form['password']

    res = badgecraft.login(username, password)
    print(res)
    if res["success"]:
        token = res["token"]
        userid = badgecraft.getId({"a": token})
        username = badgecraft.getUserName({"a": token})

        # redirect after login
        resp = make_response(redirect(url_for("overview")))
        # set cookies with current user info
        resp.set_cookie('username', username)
        resp.set_cookie('token', token)
        resp.set_cookie("userId", userid)

        return resp

    else:
        return """{"response":400}"""
