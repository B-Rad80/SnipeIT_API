#Brandon Roemer Generalized Assest Script

import configparser
import json
import requests
import os


API_KEY = "READ IN BELOW"




#Read in API_KEY
def Get_API_Key(path = "../../API_KEY.key"):
    f = open(path, "r")
    API_KEY = str(f.read())

    if "\n" in API_KEY:
           API_KEY = API_KEY[:-1]

    return API_KEY


#Read in Config


def Parse_Items(items):
    other_items = ["deleted_at","purchase_date","last_checkout","expected_checkin","purchase_cost"]
    parsed_items = []
    for i in items:
        if i.lower() == "model" or i.lower() =="model name":
            parsed_items.append(("model","name"))
        elif i.lower() == "model id":
            parsed_items.append(("model","id"))
        elif i.lower() == "category" or i.lower() == "category name":
            parsed_items.append(("category","name"))
        elif i.lower() == "category id":
            parsed_items.append(("category","id"))
        elif i.lower() == "manufacturer name" or i.lower() == "manufacturer":
            parsed_items.append(("manufacturer","name"))
        elif i.lower() == "manufacturer id":
            parsed_items.append(("manufacturer","id"))
        elif i.lower() == "status_label" or i.lower() == "status_label name":
            parsed_items.append(("status_label","name"))
        elif i.lower() == "status_label id":
            parsed_items.append(("status_label","id"))
        elif i.lower() == "status_label status_meta":
            parsed_items.append(("status_label","status_meta"))
        elif i.lower() == "created_at" or i.lower() == "created_at formatted":
            parsed_items.append(("created_at","formatted"))
        elif i.lower() == "created_at datetime":
            parsed_items.append(("created_at","datetime"))
        elif i.lower() == "updated_at" or i.lower() == "updated_at formatted":
            parsed_items.append(("updated_at","formatted"))
        elif i.lower() == "updated_at datetime":
            parsed_items.append(("updated_at","datetime"))

        elif( i.lower() == "id" or i.lower() == "name" or i.lower() == "asset_tag" or i.lower() == "serial" 
             or i.lower() == "model_number" or i.lower()== "supplier" or i.lower() == "notes" or i.lower()=="order_number" 
             or i.lower() == "company" or i.lower() == "location" or i.lower() == "rtd_location" or i.lower == "image" 
             or i.lower() == "assigned_to" or i.lower() == "warrenty_months" or i.lower() == "warrenty_expires"):
            parsed_items.append([i.lower()])
        elif(i.lower() in other_items):
            parsed_items.append([i.lower()])
        else:
            print("Item type not found" ,i, "check list of compatible items in the ReadMe")

    return parsed_items


def Read_Config(File_Name = 'config.ini'):

    sort_ID = ''
    method = "GET"
    limit = 10000

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
        except:
            raise Exception("Make sure limit is a number... Falling back on default value :", error)
    else:
        print("Using Default Limit")

    for i in config["DEFAULT"]["Companies"].split(','):
        companies.append(i)

    for k in config["DEFAULT"]["Categories_IDs"].split(','):
        categories.append(int(k))

    for l  in config["DEFAULT"]["Items"].split(','):
        items.append(l)
        print(items, "before")
    items = Parse_Items(items)
    print(items, "after")

    return items, categories, companies, limit, method, sort_ID

#Items Formatting


#Format Key
def API_CALL(param,key):
    url = "https://itll-demeter.int.colorado.edu/api/v1/hardware"
    AUTH = "Bearer " + key

    ret = []

    for j in param[1]:
        #Format Request
        querystring = {"limit": str(param[3]),
                       "offset":"0",
                       "category_id": j
                      }


        headers = {
            'authorization' : AUTH,
            'accept': "application/json",
            'content-type': "application/json"
            }

        #Make Request
        response = requests.request(param[4], url, headers=headers, params=querystring)

        #Convert to Dictionary
        #print(response.text)

        y = json.loads(response.text)
        ret.append(y)
   
    return ret


def format_output(output,items):
    cleaned_output = []
    failures = []
    companylist = []
    for fill in range(len(output)+1):
        cleaned_output.append("")

    for i in range(len(output)):
        temp = []
        for row in output[i]["rows"]:
            t_items = ""
            for k in items:
                if (not row["company"] == None ):
                    companylist.append(row["company"])
                else:
                    if (row["asset_tag"] == None):
                        raise Exception("an ITEM has no company or asset_tag")
                    else:
                        raise Exception("ITEM:",  row["asset_tag"], "has no company!")
                if len(k) == 1:
                    if(row[k[0]] == None):
                         t_items += "None,"
                    else:
                        t_items +=  str(row[k[0]])  + ","
                elif len(k) ==2:
                    if(row[k[0]][k[1]] == None):
                         t_items += "None,"
                    else:
                        t_items +=  str(row[k[0]][k[1]]) + ","
                 
                elif len(k) ==3:
                     if(row[k[0]][k[1]][k[2]]== None):
                         t_items += "None,"
                     else:
                        t_items +=  str(row[k[0]][k[1]][k[2]]) + "," 
                else:
                    raise Exception("len of item too long")

            if "None" in t_items:
                if(items.contains("asset_tag")):
                    failures.append(t_items + "\n")
                else:
                    t_items = str(i["asset_tag"]) + "," + t_items + "\n"
                    failures.append(t_items)
            else:
                temp.append(t_items[:-1])


        cleaned_output[i] = temp
        #print("added ", temp, "to cleaned_output[", i,'] is now:', cleaned_output )
        cleaned_output[len(output)] = failures
        
    return cleaned_output, companylist



         
def save_files(output,param, companylist):

    directory = os.getcwd() + "/Output/"

    if not os.path.exists(directory):
        print("Creating Directory for Output....")
        try:
            os.makedirs(directory)
        except:
            raise Exception("failed to create directory with error")

        print(output)
    print(len(companylist))
    print(len(output))
    try:
        files = {}
        ctr = 0 
        for i in range(len(param[2])):
            files[param[2][i]] = open(directory + param[2][i] + ".txt", "w")

        for j in range(0, len(output)-1):
            for index in range(len(output[j])):
                found = False
                for f in files:
                    #print(f, companylist[ctr]['name'])
                    if companylist[ctr]["name"] == f:
                        found = True 
                        files[f].writelines(output[j][index] + '\n')
                if not found:
                    print("missed,",output[j][index], companylist[ctr]['name'])
                ctr+=1


               # file.close()
        
        
            #errors =  open(directory + "failed.txt", "w")
            #errors.writelines(output[-1])
            #errors.close()
 
    except:
        raise Exception("failed to save files")

if __name__ == "__main__":
    #DO ALL THE STUFF 
   param =  Read_Config()
   print(param)
   key = Get_API_Key()
   output = API_CALL(param, key)
   #print(output)
   
   if(param[4] == "GET"):
       output,companylist = format_output(output,param[0])
       #print("output", output)
       save_files(output,param, companylist)




