import math
import random
import string
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd
import requests
from app.static.py.query_cleaner import json_to_dataframe

USERNAME = ""
PASSWORD = ""
url = 'https://www.badgecraft.eu/api/graphql'
QUERY_LIMIT = 10
TOKEN = "f30e9f7e-5f76-4119-8974-8a1b2ea164e3"
FETCHED_DATA = {}


# client = GraphqlClient(endpoint=url)



def getFetchedData():
  return FETCHED_DATA


def getId(token):
  query = f"""
    query{{
  me{{
    id
  }}
}}


  """
  result = requests.post(url, json={"query": query}, cookies=token).json()
  print(result)
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
        
      
    print(df.info())
    FETCHED_DATA = df
    return FETCHED_DATA

