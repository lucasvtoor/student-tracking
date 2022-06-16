import math
import os
import random
import string
import pandas as pd
import requests
from app.static.py.query_cleaner import json_to_dataframe
import numpy as np


# client = GraphqlClient(endpoint=url)
# define badgecraft class
class BadgeCraft:
    def __init__(self):
        self.fetched_amount = 0
        self.USERNAME = ""
        self.PASSWORD = ""
        self.url = 'https://www.badgecraft.eu/api/graphql'
        self.QUERY_LIMIT = 10
        self.TOKEN = "f30e9f7e-5f76-4119-8974-8a1b2ea164e3"
        self.FETCHED_DATA = {}
        self.projectDetails = []
        self.StudentPageOverview = []
    # get username associated with token
    def getUserName(self, token):
      # badgecraft graphql query
        query = f"""
            query{{
          me{{
            displayName
          }}
        }}


          """
        result = requests.post(self.url, json={"query": query}, cookies=token).json()
        # return query result
        return result["data"]["me"]["displayName"]

    #get user id associated token
    def getId(self, token):
        query = f"""
        query{{
      me{{
        id
        displayName
      }}
    }}


      """
        result = requests.post(self.url, json={"query": query}, cookies={"a": token}).json()
          # return query result
        return result["data"]["me"]["id"]

  # create login function (using badgecraft credentials)
    def login(self, username, password):
      # graphql query
        query = f"""
            mutation{{
                passwordAuthorize(email:"{username}",password:"{password}")
                    {{
                        success,
                        token
                    }}
            }}
        """
        result = requests.post(self.url, json={"query": query}).json()
        # return query result
        return result["data"]["passwordAuthorize"]

    # return the amout of projects in badgecraft
    def get_project_amount(self, token):
      # graphql query
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
        request = requests.post(self.url, json={"query": query}, cookies=token)
         # return query result
        return request.json()["data"]["organisations"]["list"][0]["projects"]["total"]

 # return the amout of users in badgecraft
    def get_user_amount(self, token):
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
        request = requests.post(self.url, json={"query": query}, cookies=token)
        # return query result
        return request.json()["data"]["organisations"]["list"][0]["users"]["total"]

    # create random string as alias
    def create_alias(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        return result_str


  # call all records query
    def get_records(self, user_offset, project_offset):
        alias = self.create_alias()
        return ("""
         %s :organisations(q: "Metis Montessori Lyceum - Coderclass", limit: 20) {
        list {
          projects(limit: 20, offset: %s) {
            list {
              name
              users(q: "*", limit: 100 offset:%s) {
                list {
                  team
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

    # get project status per project
    def getProjectStatus(self, fetchData, projectName):
      # make array with 3 indexes (0 = not started, 1 = in progress, 2 = done)
        scoreArr = [0, 0, 0]
        studentList = fetchData["list.projects.list.users.list.name"].unique()

        # loop through whole student list
        for student in studentList:

            # get every module accociated with given project and current student
            moduleList = fetchData.loc[((fetchData["list.projects.list.name"] == projectName) & (
                    fetchData['list.projects.list.users.list.name'] == student))]
            # get the total amount of available modules
            totalModules = moduleList["list.projects.list.users.list.badgesStatuses.list.progress"].shape[0]
            # get the total amount of completed modules by the student (if module progress is equal to 100.0)
            modulesCompleted = (moduleList["list.projects.list.users.list.badgesStatuses.list.progress"] == 100.0).sum()

            # # if completed modules is equal to total, plus 1 project list (done)
            if (modulesCompleted == totalModules and totalModules != 0):
                scoreArr[2] += 1
                # if completed modules is lower than total modules but not 0, plus 1 project list (in progress)
            if (modulesCompleted < totalModules and modulesCompleted > 0):
                scoreArr[1] += 1

                # if completed modules is equal to 0, plus 1 project list (not started)
            if (modulesCompleted == 0):
                scoreArr[0] += 1
        # return array with project status
        return scoreArr

    # retuns the badgecount per given student.
    def getbadgecount(self, data, student):
      # get all records containing students name
        df = data.loc[((data['list.projects.list.users.list.name'] == student))]
        # drop duplicates, since the badgecount per project is repeated multiple times per project
        df = df.drop_duplicates(subset=['list.projects.list.name'])
        # add all left over badges to badgeCount
        badgeCount = df['list.projects.list.users.list.stats.badges'].sum()

        return badgeCount



    # get students details progress (which module is completed or not)
    def getStudentProgress(self, data, name):
        # make copy of data, so we dont edit the main dataframe, used by the whole application
        newdf = data.copy()
        # drop unnecessary columns
        newdf.drop(newdf.columns.difference(['list.projects.list.users.list.name', 'list.projects.list.name',
                                             'list.projects.list.users.list.badgesStatuses.list.badgeClass.name',
                                             'list.projects.list.users.list.badgesStatuses.list.progress',
                                             'list.projects.list.users.list.email']), axis=1,
                   inplace=True)
        # drop empty rows
        newdf.dropna(inplace=True)

        # remove spaces to match input name for detail page
        newdf['list.projects.list.users.list.name'] = newdf['list.projects.list.users.list.name'].str.replace(" ", "")

        #get all rows for current student
        specificData = newdf.loc[((newdf['list.projects.list.users.list.name'] == name))]
        # mark module progress true or false based on completed or not(100.0)
        moduleProgress = specificData["list.projects.list.users.list.badgesStatuses.list.progress"] != 100.0
        # make new column
        specificData["module.progress"] = moduleProgress

        return specificData


        # get total progress (badgecount, quest count, certification count) per student
    def getstudentProjectCounts(self, data, student):
        # make copy of data, so we dont edit the main dataframe, used by the whole application
        df = data.copy()
        #get all rows for current student
        df = df.loc[((df['list.projects.list.users.list.name'] == student))]
        # drop dulpicates to calculate correct data
        df = df.drop_duplicates(subset=['list.projects.list.name'])

        # sum up every category
        studentBadgeCount = df["list.projects.list.users.list.stats.badges"].sum()
        studentQuestsCount = df["list.projects.list.users.list.stats.quests"].sum()
        studentCertificateCount = df["list.projects.list.users.list.stats.certificates"].sum()

        # make dict so we can transform it to a dataframe
        studentInfo = {"student.name": student, "student.badge": round(studentBadgeCount),
                       "student.quest": round(studentQuestsCount),
                       "student.certificate": round(studentCertificateCount)}

        return studentInfo

    # main fetch all data function
    def fetch(self, token=os.environ.get('TOKEN')):
        # create token 
        token = {"a": token}
        project_loop = math.ceil(self.get_project_amount(token) / self.QUERY_LIMIT)  # -1 because offset starts at 0
        user_loop = math.ceil(self.get_user_amount(token) / self.QUERY_LIMIT)  # -1 because offset starts at 0
        aliases = []
        query = "{"
        for i in range(project_loop):
            project_offset = i * self.QUERY_LIMIT
            for j in range(user_loop):
                user_offset = j * self.QUERY_LIMIT
                tup = self.get_records(user_offset, project_offset)
                query += tup[0]
                aliases.append(tup[1])

        query += "}"
        # create request
        request = requests.post(self.url, json={"query": query}, cookies=token)
        response = request.json()
        del response["errors"]
        df = pd.DataFrame()
        for alias in aliases:
            new_df = json_to_dataframe(response["data"][alias])
            df = pd.concat([df, new_df])

        # loop through student names, so we can pre render studentpage progress
        studentNames = df["list.projects.list.users.list.name"].unique()
        for student in studentNames:
            self.StudentPageOverview.append(self.getstudentProjectCounts(df, student))

        # loop through projects, so we can pre render overview project progress
        projectList = df["list.projects.list.name"].unique()
        for project in projectList:
            self.projectDetails.append(self.getProjectStatus(df, project))
            
        # assign completed fetch data to result df
        FETCHED_DATA = df
        self.FETCHED_DATA = FETCHED_DATA

# fetch data from badgecraft
