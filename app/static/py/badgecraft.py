import math
import os
import random
import string
import pandas as pd
import requests
from app.static.py.query_cleaner import json_to_dataframe
import numpy as np


# client = GraphqlClient(endpoint=url)

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

    def getUserName(self, token):
        query = f"""
            query{{
          me{{
            displayName
          }}
        }}


          """
        result = requests.post(self.url, json={"query": query}, cookies=token).json()
        print("getId::", result)
        return result["data"]["me"]["displayName"]

    def getId(self, token):
        query = f"""
        query{{
      me{{
        id
        displayName
      }}
    }}


      """
        result = requests.post(self.url, json={"query": query}, cookies=token).json()
        print("getId::", result)
        return result["data"]["me"]["id"]

    def login(self, username, password):
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
        TOKEN = result["data"]["passwordAuthorize"]["token"]
        return result["data"]["passwordAuthorize"]

    def get_project_amount(self, token):
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
        request = requests.post(self.url, json={"query": query}, cookies=token)
        return request.json()["data"]["organisations"]["list"][0]["projects"]["total"]

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
        return request.json()["data"]["organisations"]["list"][0]["users"]["total"]

    def create_alias(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(8))
        return result_str

    def not_proud_of_this(self, user_offset, project_offset):
        alias = self.create_alias()
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

    def getProjectStatus(self, fetchData, projectName):
        scoreArr = [0, 0, 0]
        studentList = fetchData["list.projects.list.users.list.name"].unique()

        # loop through student list
        for student in studentList:

            moduleList = fetchData.loc[((fetchData["list.projects.list.name"] == projectName) & (
                    fetchData['list.projects.list.users.list.name'] == student))]

            totalModules = moduleList["list.projects.list.users.list.badgesStatuses.list.progress"].shape[0]
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

    def getbadgecount(self, data, student):
        df = data.loc[((data['list.projects.list.users.list.name'] == student))]
        df = df.drop_duplicates(subset=['list.projects.list.name'])
        badgeCount = df['list.projects.list.users.list.stats.badges'].sum()

        return badgeCount

    def getStudentProgress(self, data, name):
        newdf = data.copy()
        newdf.drop(newdf.columns.difference(['list.projects.list.users.list.name', 'list.projects.list.name',
                                             'list.projects.list.users.list.badgesStatuses.list.badgeClass.name',
                                             'list.projects.list.users.list.badgesStatuses.list.progress',
                                             'list.projects.list.users.list.email']), 1,
                   inplace=True)
        newdf.dropna(inplace=True)
        newdf['list.projects.list.users.list.name'] = newdf['list.projects.list.users.list.name'].str.replace(" ", "")
        specificData = newdf.loc[((newdf['list.projects.list.users.list.name'] == name))]
        specificData["module.progress"] = np.where(
            specificData['list.projects.list.users.list.badgesStatuses.list.progress'] != 100.0, False, True)
        specificData.drop(['list.projects.list.users.list.badgesStatuses.list.progress'], 1, inplace=True)
        return specificData

    def getstudentProjectCounts(self, data, student):
      df = data.copy()
      df = df.loc[((df['list.projects.list.users.list.name'] == student))]
      df = df.drop_duplicates(subset=['list.projects.list.name'])

      studentBadgeCount = df["list.projects.list.users.list.stats.badges"].sum()
      studentQuestsCount = df["list.projects.list.users.list.stats.quests"].sum()
      studentCertificateCount = df["list.projects.list.users.list.stats.certificates"].sum()
      
      studentInfo = {"student.name": student, "student.badge": round(studentBadgeCount),"student.quest":round(studentQuestsCount),"student.certificate": round(studentCertificateCount)}

      return studentInfo

    def fetch(self, token=os.environ.get('TOKEN')):
        token = {"a": token}
        project_loop = math.ceil(self.get_project_amount(token) / self.QUERY_LIMIT)  # -1 because offset starts at 0
        user_loop = math.ceil(self.get_user_amount(token) / self.QUERY_LIMIT)  # -1 because offset starts at 0
        aliases = []
        query = "{"
        for i in range(project_loop):
            project_offset = i * self.QUERY_LIMIT
            for j in range(user_loop):
                user_offset = j * self.QUERY_LIMIT
                tup = self.not_proud_of_this(user_offset, project_offset)
                query += tup[0]
                aliases.append(tup[1])

        query += "}"
        request = requests.post(self.url, json={"query": query}, cookies=token)
        tim = request.json()
        del tim["errors"]
        df = pd.DataFrame()
        for alias in aliases:
            new_df = json_to_dataframe(tim["data"][alias])
            df = pd.concat([df, new_df])

        studentNames = df["list.projects.list.users.list.name"].unique()
        for student in studentNames:
            self.StudentPageOverview.append(self.getstudentProjectCounts(df, student))

        projectList = df["list.projects.list.name"].unique()

        for project in projectList:
            self.projectDetails.append(self.getProjectStatus(df, project))

        FETCHED_DATA = df
        self.FETCHED_DATA = FETCHED_DATA

# fetch data from badgecraft
