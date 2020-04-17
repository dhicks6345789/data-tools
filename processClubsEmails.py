#!/usr/bin/python
import os
import re
import io
import sys
import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folders exist.
clubsRoot = config["dataFolder"] + os.sep + "Clubs"
os.makedirs(clubsRoot, exist_ok=True)
emailsRoot = clubsRoot + os.sep + "Emails"
os.makedirs(emailsRoot, exist_ok=True)

# Load the user options. These are a set of simple key:values in an Excel spreadsheet. Available options:
# dateFrom: The date at which to start processing emails from. Means the user can define which emails to process rather than simply
#    processing all emails from years back.
# User: The username of the inbox to extract emails from.
options = {}
optionsDataframe = pandas.read_excel(clubsRoot + os.sep + "options.xlsx", header=None)
for optionIndex, optionValue in optionsDataframe.iterrows():
	options[optionsDataframe.at[optionIndex, 0].replace(":","").strip()] = optionsDataframe.at[optionIndex, 1]

# Use GAM to get a set of emails from GMail. The content of each email is cached locally so we don't have to query GMail for every single
# email each time the script runs.
cachedEmails = []
for emailIndex, emailValue in pandas.read_csv(io.StringIO(dataLib.runCommand("gam user " + options["user"] + " print messages query \"after:" + str(options["dateFrom"].year) + "/" + str(options["dateFrom"].month) + "/" + str(options["dateFrom"].day) + " AND from:no-reply@squarespace.com AND subject:'Knightsbridge School: A New Order has Arrived'\""))).iterrows():
	filenamePath = emailsRoot + os.sep + emailValue["id"] + ".txt"
	cachedEmails.append(emailValue["id"] + ".txt")
	if not os.path.exists(filenamePath):
		print("Caching email " + emailValue["id"] + "...")
		for emailWithBodyIndex, emailWithBodyValue in pandas.read_csv(io.StringIO(dataLib.runCommand("gam user " + options["user"] + " print messages ids " + emailValue["id"] + " showbody"))).iterrows():
			dataLib.writeFile(filenamePath, dataLib.removeBlanks(emailWithBodyValue["Body"]))
# Clear out any un-used emails from the local cache.
for cachedEmail in os.listdir(emailsRoot):
	if not cachedEmail in cachedEmails:
		os.remove(emailsRoot + os.sep + cachedEmail)
		
clubs = pandas.DataFrame(columns=["orderNumber","orderDate","orderTime","parentName","parentEmail","itemDescription","itemCode","firstChildName","firstChildClass","secondChildName","secondChildClass"])
clubs.at[1, "orderNumber"] = "123abc"
print(clubs)

sys.exit(0)

csvOutputHandle = open(config["dataFolder"] + os.sep + "Clubs" + os.sep + "clubsEmailsRawData.csv", 'w', newline='')
csvOutputWriter = csv.writer(csvOutputHandle, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
csvOutputWriter.writerow(["orderNumber","orderDate","orderTime","parentName","parentEmail","itemDescription","itemCode","firstChildName","firstChildClass","secondChildName","secondChildClass"])
for emailFilePath in os.listdir(filenameRoot):
	orderNumber = ""
	orderDate = ""
	orderTime = ""
	parentName = ""
	parentEmail = ""
	itemDescription = ""
	itemCode = ""
	firstChildName = ""
	firstChildClass = ""
	secondChildName = ""
	secondChildClass = ""
	emailText = readFile(filenameRoot + os.sep + emailFilePath)
	matchResult = re.match(".*Order #(\d*?)\. Placed on (.*?) at (\d*?:\d*? ..).*", emailText, re.DOTALL)
	if not matchResult == None:
		orderNumber = matchResult[1].strip()
		orderDate = matchResult[2].strip()
		orderTime = matchResult[3].strip()
	matchResult = re.match(".*TO:\n(.*?)\n.*\n(.*?@.*?)\n.*ITEM.*", emailText, re.DOTALL)
	if not matchResult == None:
		parentName = matchResult[1].strip()
		parentEmail = matchResult[2].strip()
	matchResult = re.match(".*SUBTOTAL\n(.*?)\n(.*?)\n.*", emailText, re.DOTALL)
	if not matchResult == None:
		itemDescription = matchResult[1].strip()
		itemCode = matchResult[2].strip()
	matchResult = re.match(".*Name of your Child:\n(.*?)\nClass/Year:\n(.*?)\nName of Second Child:(.*?)\nClass/Year:\n(.*?)\n.*", emailText, re.DOTALL)
	if not matchResult == None:
		firstChildName = matchResult[1].strip()
		firstChildClass = matchResult[2].strip()
		secondChildName = matchResult[3].strip()
		if not matchResult[4].startswith("blog <"):
			secondChildClass = matchResult[4].strip()
		csvOutputWriter.writerow([orderNumber,orderDate,orderTime,parentName,parentEmail,itemDescription,itemCode,firstChildName,firstChildClass,secondChildName,secondChildClass])
