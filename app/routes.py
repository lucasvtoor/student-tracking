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

    details = pd.DataFrame(data=badgecraft.projectDetails,columns=['not.started', 'in.progress', 'done']) 


    projectInfo = {"projectName": projectList}
    projectInfoDf = pd.DataFrame(data=projectInfo)
    projectInfoDfFinal = pd.concat([projectInfoDf, details], axis=1, join="inner")
    print(projectInfoDfFinal.head())

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
        sortingList = projectInfoDfFinal[projectInfoDfFinal['projectName'].str.contains(searchTerm, case=False, na=False)]
    else:
        sortingList = projectInfoDfFinal

    sort = request.args.get("sort")
    if sort == "assignment-asc":
        sortingList = sortingList.sort_values(by='projectName', ascending=True)

    elif sort == "assignment-desc":
        sortingList = sortingList.sort_values(by='projectName', ascending=False)

    elif sort == "not-started-asc":
        sortingList = sortingList.sort_values(by='not.started', ascending=True)

    elif sort == "not-started-desc":
        sortingList = sortingList.sort_values(by='not.started', ascending=False)

    elif sort == "in-progress-asc":
        sortingList = sortingList.sort_values(by='in.progress', ascending=True)

    elif sort == "in-progress-desc":
        sortingList = sortingList.sort_values(by='in.progress', ascending=False)
    
    elif sort == "done-asc":
        sortingList = sortingList.sort_values(by='done', ascending=True)
    
    elif sort == "done-desc":
        sortingList = sortingList.sort_values(by='done', ascending=False)
    else:
        # if `sort` is none of the above, default to showing raw list
        sortingList = sortingList


    page,per_page,offset = get_page_args(page_parameter="page",per_page_parameter="per_page")

    total = len(sortingList)

    pagination_projects_details = get_users(offset=offset,per_page=per_page, df=sortingList)

    pagination = Pagination(page=page,per_page=per_page,total=total, css_framework='bootstrap5')

    # render templates with vars
    return render_template('overview.html', fetch_amount=badgecraft.fetched_amount, protected=False,
                           student_count=len(studentCount),
                           current_user=loggedInUser, number_badges=round(totalBadgeCount), project_info=pagination_projects_details, page=page,per_page=per_page,pagination=pagination,
                           average_badgecount=averageBadgeCount, below_average_count=belowAverageCount, search_term = searchTerm)


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


    # search projects
    searchTerm = request.args.get("searchTerm")
    print(studentData.head())
    if(searchTerm != None):
        sortingList = studentData[studentData['list.projects.list.name'].str.contains(searchTerm, case=False, na=False)]
    else:
        sortingList = studentData

    sort = request.args.get("sort")
    if sort == "project-asc":
        sortingList = sortingList.sort_values(by='list.projects.list.name', ascending=True)

    elif sort == "project-desc":
        sortingList = sortingList.sort_values(by='list.projects.list.name', ascending=False)

    elif sort == "module-asc":
        sortingList = sortingList.sort_values(by='list.projects.list.users.list.badgesStatuses.list.badgeClass.name', ascending=True)

    elif sort == "module-desc":
        sortingList = sortingList.sort_values(by='list.projects.list.users.list.badgesStatuses.list.badgeClass.name', ascending=False)

    elif sort == "module-com-asc":
        sortingList = sortingList.sort_values(by='module.progress', ascending=True)

    elif sort == "module-com-desc":
        sortingList = sortingList.sort_values(by='module.progress', ascending=False)

    else:
        # if `sort` is none of the above, default to showing raw list
        sortingList = sortingList


    page,per_page,offset = get_page_args(page_parameter="page",per_page_parameter="per_page")

    total = len(sortingList)

    pagination_projects_details = get_users(offset=offset,per_page=per_page, df=sortingList)

    pagination = Pagination(page=page,per_page=per_page,total=total, css_framework='bootstrap5')


    return render_template('detail.html', protected=False, current_user=loggedInUser, student_data=pagination_projects_details, name=name, page=page,per_page=per_page,pagination=pagination, search_term = searchTerm)


def get_users(offset=0,per_page=20,df=studentInfo):
    return df[offset: offset+per_page]


# students route
@app.route('/students')
def users():
    
    loggedInUser = request.cookies.get("username")


    # search students
    searchTerm = request.args.get("searchTerm")
    if(searchTerm != None):
        sortingList = studentInfo[studentInfo['student.name'].str.contains(searchTerm, case=False, na=False)]

    else:
        sortingList = studentInfo

    sort = request.args.get("sort")
    if sort == "name-asc":
        sortingList = sortingList.sort_values(by='student.name', ascending=True)

    elif sort == "name-desc":
        sortingList = sortingList.sort_values(by='student.name', ascending=False)

    elif sort == "badge-asc":
        sortingList = sortingList.sort_values(by='student.badge', ascending=True)

    elif sort == "badge-desc":
        sortingList = sortingList.sort_values(by='student.badge', ascending=False)

    elif sort == "quest-asc":
        sortingList = sortingList.sort_values(by='student.quest', ascending=True)

    elif sort == "quest-desc":
        sortingList = sortingList.sort_values(by='student.quest', ascending=False)

    elif sort == "cert-asc":
        sortingList = sortingList.sort_values(by='student.certificate', ascending=True)

    elif sort == "cert-desc":
        sortingList = sortingList.sort_values(by='student.certificate',  ascending=False)
    else:
        # if `sort` is none of the above, default to showing raw list
        sortingList = sortingList


    page,per_page,offset = get_page_args(page_parameter="page",per_page_parameter="per_page")

    total = len(sortingList)

    pagination_users = get_users(offset=offset,per_page=per_page, df=sortingList)

    pagination = Pagination(page=page,per_page=per_page,total=total, css_framework='bootstrap5')

    return render_template('students.html', protected=False, current_user=loggedInUser, students=pagination_users,page=page,per_page=per_page,pagination=pagination, search_term = searchTerm)


# classes route
@app.route('/classes')
def classes():
    teamsDf = badgecraft.FETCHED_DATA
    teamsDf = teamsDf.rename(columns={"list.projects.list.name": "Project names","list.projects.list.users.list.team": "Teams","list.projects.list.users.list.name": "Names", "list.projects.list.users.list.email": "Emails", "list.projects.list.users.list.picture": "Pictures", "list.projects.list.users.list.stats.badges": "Badges", "list.projects.list.users.list.stats.quests": "Quests","list.projects.list.users.list.stats.certificates": "Certificates", "list.projects.list.users.list.badgesStatuses.list.status": "Status","list.projects.list.users.list.badgesStatuses.list.progress": "Progress", "list.projects.list.users.list.badgesStatuses.list.badgeClass.name": "Module"})
    teamsDf = teamsDf.drop(columns=['list.projects.list.users.list.badgesStatuses.list', 'list.projects.list.users.list.badgesStatuses'])
    
    dfCoderclassProgressionLevel1 = teamsDf[teamsDf['Module']=="Level 1"]
    progressionWithModule = (dfCoderclassProgressionLevel1['Progress']== 100).sum()
    totalRows = len(dfCoderclassProgressionLevel1.index)
    averageProgress =  (progressionWithModule /  totalRows) * 100

    dfCoderclassProgressionLevel2 = teamsDf[teamsDf['Module']=="Level 2"]
    progressionWithModule2 = (dfCoderclassProgressionLevel2['Progress']== 100).sum()
    totalRows2 = len(dfCoderclassProgressionLevel2.index)
    averageProgress2 =  (progressionWithModule2 /  totalRows2) * 100

    dfCoderclassProgressionLevel3 = teamsDf[teamsDf['Module']=="Level 3"]
    progressionWithModule3 = (dfCoderclassProgressionLevel3['Progress']== 100).sum()
    totalRows3 = len(dfCoderclassProgressionLevel3.index)
    averageProgress3 =  (progressionWithModule3 /  totalRows3) * 100

    dfCoderclassProgressionLevel4 = teamsDf[teamsDf['Module']=="Level 4"]
    progressionWithModule4 = (dfCoderclassProgressionLevel4['Progress']== 100).sum()
    totalRows4 = len(dfCoderclassProgressionLevel4.index)
    averageProgress4 =  (progressionWithModule4 /  totalRows4) * 100

    dfCoderclassProgressionLevel5 = teamsDf[teamsDf['Module']=="Level 5"]
    progressionWithModule5 = (dfCoderclassProgressionLevel5['Progress']== 100).sum()
    totalRows5 = len(dfCoderclassProgressionLevel5.index)
    averageProgress5 =  (progressionWithModule5 /  totalRows5) * 100

    dfCoderclassProgressionLevel6 = teamsDf[teamsDf['Module']=="Level 6"]
    progressionWithModule6 = (dfCoderclassProgressionLevel6['Progress']== 100).sum()
    totalRows6 = len(dfCoderclassProgressionLevel6.index)
    averageProgress6 =  (progressionWithModule6 /  totalRows6) * 100

    classes = [
        {
            'name': 'Level 1',
            'members': progressionWithModule
        },
        {
            'name': 'Level 2',
            'members': progressionWithModule2
        },
        {
            'name': 'Level 3',
            'members': progressionWithModule3
        },
        {
            'name': 'Level 4',
            'members': progressionWithModule4
        },
        {
            'name': 'Level 5',
            'members': progressionWithModule5
        },
        {
            'name': 'Level 6',
            'members': progressionWithModule6
        },
    ]

    data = [
        ("Level 1", averageProgress),
        ("Level 2", averageProgress2),
        ("Level 3", averageProgress3),
        ("Level 4", averageProgress4),
        ("Level 5", averageProgress5),
        ("Level 6", averageProgress6),
    ]

    labels = [row[0] for row in data]
    today = [row[1] for row in data]

    loggedInUser = request.cookies.get("username")
    return render_template('classes.html', classes=classes, labels=labels, today=today, protected=False,
                           current_user=loggedInUser)

@app.route('/download_student_csv')
def get_csv():
    downloadable_csv = badgecraft.FETCHED_DATA
    downloadable_csv = downloadable_csv.rename(columns={"list.projects.list.name": "Project names","list.projects.list.users.list.team": "Teams","list.projects.list.users.list.name": "Names", "list.projects.list.users.list.email": "Emails", "list.projects.list.users.list.picture": "Pictures", "list.projects.list.users.list.stats.badges": "Badges", "list.projects.list.users.list.stats.quests": "Quests","list.projects.list.users.list.stats.certificates": "Certificates", "list.projects.list.users.list.badgesStatuses.list.status": "Status","list.projects.list.users.list.badgesStatuses.list.progress": "Progress", "list.projects.list.users.list.badgesStatuses.list.badgeClass.name": "Module"})
    downloadable_csv = downloadable_csv.drop(columns=['list.projects.list.users.list.badgesStatuses.list', 'list.projects.list.users.list.badgesStatuses'])
    downloadable_csv =downloadable_csv.to_csv(index=False)
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
