#Brandon Roemer, Pull Mac Addresses 
import json
import requests
import os

#GLOBAL VARIABLES INIT
API_KEY = "READ IN BELOW"
url = "https://itll-demeter.int.colorado.edu/api/v1/hardware"

IF_MAC = []
ITLP_MAC = []
AES_MAC = []
NULL_MAC = ["Name","Asset_Tag","Location"]

##########################################################################
#                              API_CALL                                  #
##########################################################################

#Read in KEY
f = open("API_KEY.txt", "r")
API_KEY = str(f.read())[:-1]

#Format Request
AUTH = "Bearer " + API_KEY
categories = ["87","79"]

for j in categories:
    querystring = {"limit":"100000",
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

    #print(response.text) #Debug

    #Convert to Dictionary
    y = json.loads(response.text)

    for item in y["rows"]:
        if item["custom_fields"]["MAC Address"]["value"] == None:
            try:
                NULL_MAC.append(str(str(item["name"]) + "," + str(item["asset_tag"]) + "," + str(item["location"]["name"]) + '\n'))
            except:
                NULL_MAC.append(str(str(item["name"]) + "," + str(item["asset_tag"]) + "," + str(item["location"]) + '\n'))

        elif item["company"]["name"] == "ITLP":
            ITLP_MAC.append(item["custom_fields"]["MAC Address"]["value"] + "\n")
        elif item["company"]["name"] == "IF":
            IF_MAC.append(item["custom_fields"]["MAC Address"]["value"] + "\n")
        elif item["company"]["name"] == "AES":
            AES_MAC.append(item["custom_fields"]["MAC Address"]["value"] + "\n")

#Print Values
print("\n\n--------------ITLP--------------")
print(IF_MAC)
print("\n\n---------------IF---------------")
print(ITLP_MAC)
print("\n\n--------------AES---------------")
print(AES_MAC)
print("\n\n-----------NULL VALUE-----------")
print(NULL_MAC)
print("\n")

##########################################################################
#                         Save to Text/CSV                               #
##########################################################################
print("Saving...\n ***This will OVERWITE ALL relavent files****")

#Vars
directory = os.getcwd() + "/Mac_Addresses"
if not os.path.exists(directory):
    print("Creating Directory for Mac Addreses....")
    os.makedirs(directory)

ITLP_F = open(directory + "/ITLP_MAC.txt", "w")
IF_F = open(directory + "/IF_MAC.txt", "w")
AES_F = open(directory + "/AES_MAC.txt", "w")
NULL_F = open(directory + "/NULL_MAC.csv", "w")



#Write Files.... overwrites existing data
try:
    ITLP_F.writelines(ITLP_MAC)
    print("Saved ITLP")
    IF_F.writelines(IF_MAC)     
    print("Saved IF")
    AES_F.writelines(AES_MAC)
    print("Saved AES")
    NULL_F.writelines(NULL_MAC)
    print("Saved NULL")
except:
    print("Line 90: Failed to Save Files")

print("\n")




       

#Close Files
ITLP_F.close()
IF_F.close()
AES_F.close()
NULL_F.close()
print("Done")

