import math
import random
import string
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import requests
from app.static.py.query_cleaner import json_to_dataframe
import numpy as np

USERNAME = ""
PASSWORD = ""
url = 'https://www.badgecraft.eu/api/graphql'
QUERY_LIMIT = 10
TOKEN = "f30e9f7e-5f76-4119-8974-8a1b2ea164e3"
FETCHED_DATA = {}
projectDetails = []
StudentPageOverview = []


# client = GraphqlClient(endpoint=url)


def getUsername(token):
  query = f"""
    query{{
  me{{
    displayName
  }}
}}


  """
  result = requests.post(url, json={"query": query}, cookies=token).json()
  print("getId::", result)
  return result["data"]["me"]["displayName"]


def getId(token):
  query = f"""
    query{{
  me{{
    id
    displayName
  }}
}}


  """
  result = requests.post(url, json={"query": query}, cookies=token).json()
  print("getId::", result)
  return result["data"]["me"]["id"]



def login(username, password):
    query = f"""
        mutation{{
            passwordAuthorize(email:"{username}",password:"{password}")
                {{
                    success,
                    token
                }}
        }}
    """
    result = requests.post(url, json={"query": query}).json()
    TOKEN = result["data"]["passwordAuthorize"]["token"]
    return result["data"]["passwordAuthorize"]


def get_project_amount(token):
    query = """
  query {
    organisations (q:"Metis Montessori Lyceum - Coderclass"){
      list {
        projects {
          total
        }
      }
    }
  }
"""
    print(token)
    request = requests.post(url, json={"query": query}, cookies=token)
    return request.json()["data"]["organisations"]["list"][0]["projects"]["total"]


def get_user_amount(token):
    query = """
  query {
  organisations (q:"Metis Montessori Lyceum - Coderclass"){
    list {
    	users {
        total
   	  }
  	}
  }
}
"""
    request = requests.post(url, json={"query": query}, cookies=token)
    return request.json()["data"]["organisations"]["list"][0]["users"]["total"]


def create_alias():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(8))
    return result_str


"""
    generates query with proper offsets and an alias to be appended to megaquery.
    This is legit the fastest method I've been able to figure out.
"""


def not_proud_of_this(user_offset, project_offset):
    alias = create_alias()
    return ("""
     %s :organisations(q: "Metis Montessori Lyceum - Coderclass", limit: 20) {
    list {
      projects(limit: 20, offset: %s) {
        list {
          name
          users(q: "*", limit: 100 offset:%s) {
            list {
              name
              email
              picture
              stats{
                badges
                quests
                certificates
              }
              badgesStatuses {
                list {
                  status
                  progress
                  badgeClass {
                    name
                  }
                }
              }
            }
          }
        }
      }
    }
    }
    
    """ % (alias, project_offset, user_offset), alias)


# get project status per projoct
def getProjectStatus(fetchData, projectName):
    scoreArr = [0,0,0]
    studentList = fetchData["list.projects.list.users.list.name"].unique()

    # loop through student list
    for student in studentList:

        moduleList = fetchData.loc[((fetchData["list.projects.list.name"] == projectName) & (fetchData['list.projects.list.users.list.name'] == student))]

        totalModules = moduleList["list.projects.list.users.list.badgesStatuses.list.progress"].shape[0]
        modulesCompleted = (moduleList["list.projects.list.users.list.badgesStatuses.list.progress"] == 100.0).sum()

        # # if completed modules is equal to total, plus 1 project list (done)
        if(modulesCompleted == totalModules and totalModules != 0):   
            scoreArr[2] += 1
            # if completed modules is lower than total modules but not 0, plus 1 project list (in progress)
        if(modulesCompleted < totalModules and modulesCompleted > 0):
            scoreArr[1] += 1

            # if completed modules is equal to 0, plus 1 project list (not started)
        if(modulesCompleted == 0):
            scoreArr[0] += 1
    # return array with project status 
    return scoreArr

# calculate badgecount per student
def getbadgecount(data, student):
    df = data.loc[((data['list.projects.list.users.list.name'] == student))]
    df = df.drop_duplicates(subset=['list.projects.list.name'])
    badgeCount = df['list.projects.list.users.list.stats.badges'].sum()
      
    return badgeCount

#Detail info student
# def getStudentProgress(data, student):
#    data.drop(data.columns.difference(['list.projects.list.users.list.name','list.projects.list.name', 'list.projects.list.users.list.badgesStatuses.list.badgeClass.name', 'list.projects.list.users.list.badgesStatuses.list.progress']), 1, inplace=True)
   
   
#    specificData = data.loc[((data['list.projects.list.users.list.name'] == student))]
#    specificData["module.progress"] = np.where(specificData['list.projects.list.users.list.badgesStatuses.list.progress'] != 100.0, False, True)
#    specificData.drop(['list.projects.list.users.list.badgesStatuses.list.progress'], 1, inplace=True)

#    return specificData


def getStudentProgress(data, name):
    newdf = data.copy()
    newdf.drop(newdf.columns.difference(['list.projects.list.users.list.name','list.projects.list.name', 'list.projects.list.users.list.badgesStatuses.list.badgeClass.name', 'list.projects.list.users.list.badgesStatuses.list.progress']), 1, inplace=True)
    newdf.dropna(inplace=True)
    newdf['list.projects.list.users.list.name'] = newdf['list.projects.list.users.list.name'].str.replace(" ","")
    specificData = newdf.loc[((newdf['list.projects.list.users.list.name'] == name))]
    specificData["module.progress"] = np.where(specificData['list.projects.list.users.list.badgesStatuses.list.progress'] != 100.0, False, True)
    specificData.drop(['list.projects.list.users.list.badgesStatuses.list.progress'], 1, inplace=True)
    return specificData 



def getstudentProjectCounts(data, student):
    studentInfo = [0,0,0]
    df = data.copy()
    df = df.loc[((df['list.projects.list.users.list.name'] == student))]
    df = df.drop_duplicates(subset=['list.projects.list.name'])
    studentBadgeCount = df["list.projects.list.users.list.stats.badges"].sum()
    studentQuestsCount = df["list.projects.list.users.list.stats.quests"].sum()
    studentCertificateCount = df["list.projects.list.users.list.stats.certificates"].sum()
    
    studentInfo = [round(studentBadgeCount),round(studentQuestsCount),round(studentCertificateCount)]

    return studentInfo  


# fetch data from badgecraft
def fetch(token):
    token = {"a": token}
    project_loop = math.ceil(get_project_amount(token) / QUERY_LIMIT)  # -1 because offset starts at 0
    user_loop = math.ceil(get_user_amount(token) / QUERY_LIMIT)  # -1 because offset starts at 0
    aliases = []
    query = "{"
    for i in range(project_loop):
        project_offset = i * QUERY_LIMIT
        for j in range(user_loop):
            user_offset = j * QUERY_LIMIT
            tup = not_proud_of_this(user_offset, project_offset)
            query += tup[0]
            aliases.append(tup[1])

    query += "}"
    request = requests.post(url, json={"query": query}, cookies=token)
    tim = request.json()
    del tim["errors"]
    df = pd.DataFrame()
    for alias in aliases:
        new_df = json_to_dataframe(tim["data"][alias])
        df = pd.concat([df, new_df])
    
    studentNames = df["list.projects.list.users.list.name"].unique()
    for student in studentNames:
      StudentPageOverview.append(getstudentProjectCounts(df, student))
    

    projectList = df["list.projects.list.name"].unique()

    for project in projectList:
      projectDetails.append(getProjectStatus(df, project))
        
    FETCHED_DATA = df
    return FETCHED_DATA


