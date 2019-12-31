Brandon Roemer Generalized Assest Script

Bug list\
Doesnt seperate by company but by category? \
Fix via adding check and seperation in format output or api call 

Test list\
Tested with model name or model \
tested with changed limits \
NEEDS multiple categories check 

##needed features##\
GET integration is working\
Expand Parsed Item options \
POST integration


[DEFAULT]\
#Generate this via snipe sign in as the user with correct perms and click on the name of the user in the top right and select "Manage API Keys" -> create new token\
#POST/PATCH (Update) or GET \
Method = GET \
#This will split output files into seperate companies listed
#Comma seperated for list(s)
Companies = ITLL,IDF	\
Categories_IDs =  79	\
#List of things wanted/to be updated EX: macaddress,name,assettag, see readme for full list\
Items = asset_tag	\
#ID Specify the column name you wish to sort by see here for list https://snipe-it.readme.io/v4.0/reference#hardware-list\	
Sort_By_ID = 	\
Limit =	10

