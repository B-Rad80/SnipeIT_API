#Brandon Roemer Updates Asset Names
import json
import requests
import os

#GLOBAL VARIABLES INIT
API_KEY = "READ IN BELOW"
url = "https://itll-demeter.int.colorado.edu/api/v1/hardware"

#Read in Data
Updated_Names = [("asset tag","Name")]



#Read in KEY
f = open("ASSET_API_KEY.txt", "r")
API_KEY = str(f.read())[:-1]

#Format Request
AUTH = "Bearer " + API_KEY