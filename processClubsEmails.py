#!/usr/bin/python
import os
import re
import io
import sys
import pandas
import dataLib

# A function to remove "nan" strings from data - /really/ shouldn't be needed...
def noNan(theString):
	if str(theString) == "nan" or str(theString) == "0":
		return ""
	return str(theString)

def normaliseDescription(theDescription):
	result = ""
	for theChar in theDescription:
		if theChar in "1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz/-();£& ":
			result = result + theChar
	return result.replace("/","-").replace("&amp;","&").strip()

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folders exist.
clubsRoot = config["dataFolder"] + os.sep + "Clubs"
os.makedirs(clubsRoot, exist_ok=True)
emailsRoot = clubsRoot + os.sep + "Emails"
os.makedirs(emailsRoot, exist_ok=True)
csvsRoot = clubsRoot + os.sep + "CSVs"
os.makedirs(csvsRoot, exist_ok=True)

# Load the user options. These are a set of simple key:values in an Excel spreadsheet. Available options:
# dateFrom: The date at which to start processing emails from. Means the user can define which emails to process rather than simply
#    processing all emails from years back.
# User: The username of the inbox to extract emails from.
options = {}
clubDescriptions = {}
teachers = []
optionsDataframe = pandas.read_excel(clubsRoot + os.sep + "options.xlsx", header=None)
for optionIndex, optionValue in optionsDataframe.iterrows():
	if not optionIndex == 0:
		optionName = noNan(optionsDataframe.at[optionIndex, 0]).replace(":","").strip()
		if not optionName == "":
			options[optionName] = optionsDataframe.at[optionIndex, 1]
		clubDescription = noNan(optionsDataframe.at[optionIndex, 2]).replace(":","").strip()
		clubAccount = noNan(optionsDataframe.at[optionIndex, 3]).replace(":","").strip()
		if not clubDescription == "" and not clubAccount == "":
			clubDescriptions[clubDescription] = clubAccount
		teacher = noNan(optionsDataframe.at[optionIndex, 4]).strip()
		if not teacher == "":
			teachers.append(teacher)

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

# Read the existing clubs data from an Excel file, or crate a new one if needed.
rawDataChanged = False
rawDataRoot = clubsRoot + os.sep + "clubsEmailsRawData.xlsx"
clubsColumns = ["orderNumber","orderDate","orderTime","parentName","parentEmail","itemDescription","itemCode","firstChildName","firstChildClass","firstChildUsername","secondChildName","secondChildClass","secondChildUsername"]
if os.path.exists(rawDataRoot):
	clubs = pandas.read_excel(rawDataRoot, dtype=str)
else:
	rawDataChanged = True
	clubs = pandas.DataFrame(columns=clubsColumns)

# Go through each email and extract data.
emailIndex = len(clubs.index)
existingOrderNumbers = clubs["orderNumber"].tolist()
for emailFilePath in os.listdir(emailsRoot):
	orderNumber = ""
	emailText = dataLib.readFile(emailsRoot + os.sep + emailFilePath)
	matchResult = re.match(".*Order #(\d*?)\. Placed on (.*?) at (\d*?:\d*? ..).*", emailText, re.DOTALL)
	if not matchResult == None:
		orderNumber = matchResult[1].strip()
	if not orderNumber in existingOrderNumbers:
		result = {}
		rawDataChanged = True
		result["orderNumber"] = matchResult[1].strip()
		result["orderDate"] = matchResult[2].strip()
		result["orderTime"] = matchResult[3].strip()
		matchResult = re.match(".*TO:\n(.*?)\n.*\n(.*?@.*?)\n.*ITEM.*", emailText, re.DOTALL)
		if not matchResult == None:
			result["parentName"] = matchResult[1].strip()
			result["parentEmail"] = matchResult[2].strip()
		matchResult = re.match(".*Name of your Child:\n(.*?)\nClass/Year:\n(.*?)\nName of Second Child:(.*?)\nClass/Year:\n(.*?)\n.*", emailText, re.DOTALL)
		if not matchResult == None:
			result["firstChildName"] = matchResult[1].strip()
			result["firstChildClass"] = matchResult[2].strip()
			result["secondChildName"] = matchResult[3].strip()
			if matchResult[4].startswith("blog <"):
				result["secondChildClass"] = ""
			else:
				result["secondChildClass"] = matchResult[4].strip()
		#matchResult = re.match(".*SUBTOTAL\n(.*?)\n(.*?)\n.*", emailText, re.DOTALL)
		matchResult = re.match(".*SUBTOTAL(.*?)TOTAL", emailText, re.DOTALL)
		if not matchResult == None:
			itemDescription = ""
			for resultLine in matchResult[1].split("\n"):
				if resultLine.strip().startswith("SQ"):
					clubs.at[emailIndex, "itemDescription"] = itemDescription
					clubs.at[emailIndex, "itemCode"] = resultLine.strip()
					for field in result.keys():
						clubs.at[emailIndex, field] = result[field]
					emailIndex = emailIndex + 1
				else:
					itemDescription = normaliseDescription(resultLine.strip())

# Make sure the "clubs" DataFrame is formatted as strings, and remove any "nan" values.
clubs = clubs.astype(str)
for clubIndex, clubValue in clubs.iterrows():
	for clubsColumn in clubsColumns:
		clubs.at[clubIndex, clubsColumn] = noNan(clubs.at[clubIndex, clubsColumn])
		
# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Try and match up pupil name strings (which are from a free-typed input box, so might have errors) and usernames.
for clubIndex, clubValue in clubs.iterrows():
	firstChildName = clubs.at[clubIndex, "firstChildName"].lower().strip()
	secondChildName = clubValue["secondChildName"].lower().strip()
	for pupilIndex, pupilValue in pupils.iterrows():
		pupilName = pupilValue["GivenName"].lower() + " " +  pupilValue["FamilyName"].lower()
		if pupilName == firstChildName and clubValue["firstChildUsername"] == "":
			clubs.at[clubIndex, "firstChildUsername"] = pupilValue["OldUsername"]
			rawDataChanged = True
		if pupilName == secondChildName and clubValue["secondChildUsername"] == "":
			clubs.at[clubIndex, "secondChildUsername"] = pupilValue["OldUsername"]
			rawDataChanged = True
			
# We only write out a new Excel file if some data has actually changed, that way we don't re-sync an identical file to Google Drive
# every time we run.
if rawDataChanged:
	print("Writing " + rawDataRoot)
	clubs.to_excel(rawDataRoot, index=False)

# Get a current list of Google Classrooms.
classrooms =  pandas.read_csv(io.StringIO(dataLib.runCommand("gam print courses")))
	
# Generate a list of clubs.
clubMembers = {}
for clubIndex, clubValue in clubs.iterrows():
	if not clubValue["itemDescription"] == "":
		clubMembers[clubValue["itemDescription"]] = []

# Assign pupils to each club and write out a CSV file of members for each one.
changedClubMembers = {}
for clubName in clubMembers.keys():
	for clubIndex, clubValue in clubs.iterrows():
		if not clubValue["firstChildUsername"] == "" and clubValue["itemDescription"] == clubName:
			clubMembers[clubName].append(clubValue["firstChildUsername"])
		if not clubValue["secondChildUsername"] == "" and clubValue["itemDescription"] == clubName:
			clubMembers[clubName].append(clubValue["secondChildUsername"])
	currentCSV = ""
	csvPath = csvsRoot + os.sep + clubName + ".csv"
	if os.path.exists(csvPath):
		currentCSV = dataLib.readFile(csvPath)
	newCSV = "\n".join(clubMembers[clubName]).strip()
	if not currentCSV == newCSV:
		print("Writing " + clubName + ".csv")
		dataLib.writeFile(csvPath, newCSV)
		changedClubMembers[clubName] = clubMembers[clubName]

# For each club listed in the options sheet, make sure a matching Google Classroom exists and set teachers and pupil membership.
for clubDescription in clubDescriptions.keys():
	classroomID = ""
	for classroomIndex, classroomValue in classrooms.iterrows():
		if classroomValue["name"] == clubDescription:
			classroomID = str(classroomValue["id"])
	if classroomID == "":
		os.system("gam create course name \"" + clubDescription + "\" teacher " + clubDescriptions[clubDescription] + " status ACTIVE")
	else:
		dataLib.writeFile("classroomTeachers.csv", "\n".join(teachers) + "\n" + clubDescriptions[clubDescription].replace(",","\n"))
		os.system("gam course " + classroomID + " sync teachers file classroomTeachers.csv")
		os.remove("classroomTeachers.csv")
		if clubDescription in changedClubMembers.keys():
			#for clubMember in clubMembers[clubDescription]:
			#	os.system("gam course " + classroomID + " add student " + clubMember)
			os.system("gam course " + classroomID + " sync students file \"" + csvsRoot + os.sep + clubDescription + ".csv\"")
