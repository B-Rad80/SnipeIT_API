#Brandon Roemer Updates Asset Names
import configparser
import json
import requests
import os

##########################################################################
#                      GLOBAL/DEFAULT VARIABLES                          #
##########################################################################
API_KEY = "READ IN BELOW"
url = "https://itll-demeter.int.colorado.edu/api/v1/hardware"

sort_ID = ''
method = ''
limit = 1

companies = []
categories = []
items = []

config = configparser.ConfigParser()


#Read in API_KEY
def Get_API_Key(path = "../../API_KEY.key"):
    f = open(path, "r")
    API_KEY = str(f.read())

    if "\n" in API_KEY:
           API_KEY = API_KEY[:-1]


##########################################################################
#                         CONFIGURATION FILE                             #
##########################################################################
#Read in Config

def Read_Config(File_Name = 'config.ini'):

    config.read('config.ini')

    print(config["DEFAULT"]["METHOD"])
    sort_ID = config["DEFAULT"]["Sort_By_ID"]
    method = str(config["DEFAULT"]["METHOD"])


    if config["DEFAULT"]["Limit"] != '':
        try:
            limit = int(config["DEFAULT"]["Limit"]) 
        except error:
            print("Make sure limit is a number... Falling back on default value :", error)

    for i in config["DEFAULT"]["Companies"].split(','):
        companies.append(i)

    for k in config["DEFAULT"]["Categories_IDs"].split(','):
        categories.append(int(k))

    for l  in config["DEFAULT"]["Items"].split(','):
        items.append(l)

#Items Formatting


##########################################################################
#                              API_CALL                                  #
##########################################################################

#Format Key
def API_CALL():
    AUTH = "Bearer " + API_KEY

    for j in categories:
        #Format Request
        querystring = {"limit":limit,
                       "offset":"0",
                       "category_id": j
                      }


        headers = {
            'authorization' : AUTH,
            'accept': "application/json",
            'content-type': "application/json"
            }

        #Make Request
        print("method", method)
        response = requests.request(method, url, headers=headers, params=querystring)

        #Convert to Dictionary
        print(response.text)
        y = json.loads(response.text)
    print(y)
    '''
    for item in y["rows"]:
        for comp in companies:
            for var in vars:
                if(len(var[i]) == 3):
                    for item[var][var][var]:
                        print("d")
    '''
         
##########################################################################
#                         Save to Text/CSV                               #
##########################################################################

print("here, dumb colors") #Debug

if __name__ == "__main__":
    #DO ALL THE STUFF 
    Read_Config()
    Get_API_Key()
    API_CALL()



