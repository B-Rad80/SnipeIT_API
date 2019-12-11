#Brandon Roemer Generalized Assest Script
import configparser
import json
import requests
import os


API_KEY = "READ IN BELOW"
url = "https://itll-demeter.int.colorado.edu/api/v1/hardware"




#Read in API_KEY
def Get_API_Key(path = "../../API_KEY.key"):
    f = open(path, "r")
    API_KEY = str(f.read())

    if "\n" in API_KEY:
           API_KEY = API_KEY[:-1]

    return API_KEY


#Read in Config

def Parse_Items(items):
    parsed_items = []
    for i in items:
        if i.lower() == "model" or "model name":
            parsed_items.append(("model","name"))
        elif i.lower() == "model id":
            parsed_items.append(("model","id"))
        elif i.lower() == "id" or i.lower() == "name" or i.lower() == "asset_tag" or i.lower() == "serial":
            parsed_items.append(i.lower())
        else:
            print("Item type not found" ,i, "check list of compatible items in the ReadMe")

    return parsed_items


def Read_Config(File_Name = 'config.ini'):

    sort_ID = ''
    method = "GET"
    limit = 1

    companies = []
    categories = []
    items = []

    config = configparser.ConfigParser()

    config.read('config.ini')

    print(config["DEFAULT"]["METHOD"])
    sort_ID = config["DEFAULT"]["Sort_By_ID"]
    if str(config["DEFAULT"]["METHOD"]) != '':
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
    items = Parse_Items(items)

    return items, categories, companies, limit, method, sort_ID

#Items Formatting


#Format Key
def API_CALL(param,key):
    AUTH = "Bearer " + key

    ret = []

    for j in param[1]:
        #Format Request
        querystring = {"limit":param[3],
                       "offset":"0",
                       "category_id": j
                      }


        headers = {
            'authorization' : AUTH,
            'accept': "application/json",
            'content-type': "application/json"
            }

        #Make Request
        print("method", param[4])
        response = requests.request(param[4], url, headers=headers, params=querystring)

        #Convert to Dictionary
        print(response.text)

        y = json.loads(response.text)
        ret.append(y)
    print("ret:\n",ret,"\nEnd Ret")
   
    return ret


def format_output(output,items):
    cleaned_output = []
    t_failures = []
    for fill in range(len(output)+1):
        cleaned_output.append("empty")

    for i in range(len(output)):
        temp = []
        for row in output[i]["rows"]:
            t_items = []
            failed = False
            for k in items:
                if len(k) == 1:
                    if(row[k] == None):
                         t_items.append("None")
                    else:
                        t_items.append(row[k])
                elif len(k) ==2:
                    if(row[k[0]][k[1]] == None):
                         t_items.append("None")
                    else:
                        t_items.append(row[k[0]][k[1]])
                 
                elif len(k) ==3:
                     if(row[k[0]][k[1]][k[2]]== None):
                         t_items.append("None")
                     else:
                        t_items.append(row[k[0]][k[1]][k[2]])
                else:
                    raise Exception("len of item too long")

        if "None" in t_items:
            if(items.contains("asset_tag")):
                t_failures.append(t_items)
            else:
                t_items.append(i["asset_tag"])
                t_failures.append(t_items)

            temp.append(t_items)
        cleaned_output[i] == temp
        cleaned_output[len(output)-1] = t_failures
        
    return cleaned_output



         
def save_files(output,param):

    directory = os.getcwd() + "/Output"

    if not os.path.exists(directory):
        print("Creating Directory for Output....")
        try:
            os.makedirs(directory)
        except:
            raise Exception("failed to create directory with error")

    try:
        for i in range(len(companies)):
            file = open(directory + param[2][i] + ".txt", "w")
            file.writelines(output[i])
            file.close()

        file = open(directory + "failed.txt", "w")
        file.writelines(output[-1])
        file.close()
    except:
        raise Exception("failed to save files")

if __name__ == "__main__":
    #DO ALL THE STUFF 
   param =  Read_Config()
   print(param)
   key = Get_API_Key()
   output = API_CALL(param, key)
   print(output)
   
   if(param[4] == "GET"):
       output = format_output(output,param[0])
       save_files(output,param)




