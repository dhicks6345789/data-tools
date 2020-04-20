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
		
rawDataChanged = False
rawDataRoot = clubsRoot + os.sep + "clubsEmailsRawData.xlsx"
if os.path.exists(rawDataRoot):
	clubs = pandas.read_excel(rawDataRoot)
else:
	rawDataChanged = True
	clubs = pandas.DataFrame(columns=["orderNumber","orderDate","orderTime","parentName","parentEmail","itemDescription","itemCode","firstChildName","firstChildClass","firstChildUsername","secondChildName","secondChildClass","secondChildUsername"])

# Go through each email and extract data.
emailIndex = len(clubs.index)
existingOrderNumbers = clubs["orderNumber"].tolist()
for emailFilePath in os.listdir(emailsRoot):
	orderNumber = 0
	emailText = dataLib.readFile(emailsRoot + os.sep + emailFilePath)
	matchResult = re.match(".*Order #(\d*?)\. Placed on (.*?) at (\d*?:\d*? ..).*", emailText, re.DOTALL)
	if not matchResult == None:
		try:
			orderNumber = int(matchResult[1].strip())
		except ValueError:
			orderNumber = 0
	if not orderNumber == 0 and not orderNumber in existingOrderNumbers:
		rawDataChanged = True
		clubs.at[emailIndex, "orderNumber"] = matchResult[1].strip()
		clubs.at[emailIndex, "orderDate"] = matchResult[2].strip()
		clubs.at[emailIndex, "orderTime"] = matchResult[3].strip()
		matchResult = re.match(".*TO:\n(.*?)\n.*\n(.*?@.*?)\n.*ITEM.*", emailText, re.DOTALL)
		if not matchResult == None:
			clubs.at[emailIndex, "parentName"] = matchResult[1].strip()
			clubs.at[emailIndex, "parentEmail"] = matchResult[2].strip()
		matchResult = re.match(".*SUBTOTAL\n(.*?)\n(.*?)\n.*", emailText, re.DOTALL)
		if not matchResult == None:
			clubs.at[emailIndex, "itemDescription"] = matchResult[1].strip()
			clubs.at[emailIndex, "itemCode"] = matchResult[2].strip()
		matchResult = re.match(".*Name of your Child:\n(.*?)\nClass/Year:\n(.*?)\nName of Second Child:(.*?)\nClass/Year:\n(.*?)\n.*", emailText, re.DOTALL)
		if not matchResult == None:
			clubs.at[emailIndex, "firstChildName"] = matchResult[1].strip()
			clubs.at[emailIndex, "firstChildClass"] = matchResult[2].strip()
			clubs.at[emailIndex, "secondChildName"] = matchResult[3].strip()
			if matchResult[4].startswith("blog <"):
				clubs.at[emailIndex, "secondChildClass"] = ""
			else:
				clubs.at[emailIndex, "secondChildClass"] = matchResult[4].strip()
		emailIndex = emailIndex + 1

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

for clubIndex, clubValue in clubs.iterrows():
	firstChildName = clubValue["firstChildName"].lower().strip()
	secondChildName = clubValue["secondChildName"].lower().strip()
	for pupilIndex, pupilValue in pupils.iterrows():
		pupilName = pupilValue["givenName"].lower() + " " +  pupilValue["familyName"].lower()
		if pupilName == firstChildName AND clubValue["firstChildUsername"] == "":
			clubs.at[clubIndex, "firstChildUsername"] = pupilValue["oldUsername"]
			rawDataChanged = True

if rawDataChanged:
	clubs.to_excel(rawDataRoot)
