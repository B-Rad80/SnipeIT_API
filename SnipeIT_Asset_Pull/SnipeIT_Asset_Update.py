#Brandon Roemer Updates Asset Names
import json
import requests
import os

#GLOBAL VARIABLES INIT
API_KEY = "READ IN BELOW"
url = "https://itll-demeter.int.colorado.edu/api/v1/hardware"



#Read in Config
f = open("API_KEY.txt", "r")
API_KEY = str(f.read())[:-1]

#Format Request
AUTH = "Bearer " + API_KEY

catagories = ["57"]
companies = False
for i in catagories:
    querystring = {"limit":"1",
                        "offset":"0",
                        "category_id": j
                        }

    #print(AUTH) #Debug 
    headers = {
        'authorization' : AUTH,
        'accept': "application/json",
        'content-type': "application/json"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    #Convert to Dictionary
    y = json.loads(response.text)
    print(y)

    #for item in y["rows"]:
        

          


#print(response.text) #Debug


