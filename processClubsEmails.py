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

# Writes out the given data to the given file, but only if the data has changed. Returns True if there was a change, False if not.
def writeCSV(csvPath, newCSV):
	currentCSV = ""
	if os.path.exists(csvPath):
		currentCSV = dataLib.readFile(csvPath)
	if not currentCSV == newCSV:
		print("Writing " + csvPath)
		dataLib.writeFile(csvPath, newCSV)
		return True
	return False

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folders exist.
clubsRoot = config["dataFolder"] + os.sep + "Clubs"
os.makedirs(clubsRoot, exist_ok=True)
emailsRoot = clubsRoot + os.sep + "Emails"
os.makedirs(emailsRoot, exist_ok=True)
csvsRootStudents = clubsRoot + os.sep + "CSVs" + os.sep + "Students"
os.makedirs(csvsRootStudents, exist_ok=True)
csvsRootTeachers = clubsRoot + os.sep + "CSVs" + os.sep + "Teachers"
os.makedirs(csvsRootTeachers, exist_ok=True)

if len(sys.argv) > 1:
	if sys.argv[1] == "-flushCache":
		print("erase \"" + csvsRootStudents + os.sep + "*.csv\"")
		print("erase \"" + csvsRootTeachers + os.sep + "*.csv\"")

# Load the user options. These are a set of simple key:values in an Excel spreadsheet. Available options:
# dateFrom: The date at which to start processing emails from. Means the user can define which emails to process rather than simply
#    processing all emails from years back.
# User: The username of the inbox to extract emails from.
options = {}
teachers = []
optionsDataframe = pandas.read_excel(clubsRoot + os.sep + "options.xlsx", header=None)
for optionIndex, optionValue in optionsDataframe.iterrows():
	if not optionIndex == 0:
		optionName = noNan(optionsDataframe.at[optionIndex, 0]).replace(":","").strip()
		if not optionName == "":
			options[optionName] = optionsDataframe.at[optionIndex, 1]
		teacher = noNan(optionsDataframe.at[optionIndex, 2]).strip()
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
		
# Read the existing list of clubs from an Excel file, or create a new one if needed.
clubsListChanged = False
clubsListRoot = clubsRoot + os.sep + "clubsList.xlsx"
clubsListColumns = ["club","teacher"]
if os.path.exists(clubsListRoot):
	clubsList = pandas.read_excel(clubsListRoot, dtype=str)
else:
	clubsListChanged = True
	clubsList = pandas.DataFrame(columns=clubsListColumns)

# Read the existing clubs data from an Excel file, or create a new one if needed.
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
			
# We only write out a new Excel file if some data has actually changed, that
# way we don't re-sync an identical file to Google Drive every time we run.
if rawDataChanged:
	print("Writing " + rawDataRoot)
	clubs.to_excel(rawDataRoot, index=False)

# Get a current list of Google Classrooms.
classrooms =  pandas.read_csv(io.StringIO(dataLib.runCommand("gam print courses")))
	
# Generate a list of clubs from the emails.
clubMembers = {}
for clubIndex, clubValue in clubs.iterrows():
	if not clubValue["itemDescription"] == "":
		clubMembers[clubValue["itemDescription"]] = []

clubsListEnd = len(clubsList)
clubsListNames = clubsList["club"].tolist()
for clubName in clubMembers.keys():
	if not clubName in clubsListNames:
		print("New club: " + clubName)
		clubsList.at[clubsListEnd, "club"] = clubName
		clubsList.at[clubsListEnd, "teacher"] = ""
		clubsListChanged = True
		clubsListEnd = clubsListEnd + 1
		
# Make sure the "clubsList" DataFrame is formatted as strings, and remove any "nan" values.
clubsList = clubsList.astype(str)
for clubsListIndex, clubsListValue in clubsList.iterrows():
	for clubsListColumn in clubsListColumns:
		clubs.at[clubsListIndex, clubsListColumn] = noNan(clubsList.at[clubsListIndex, clubsListColumn])

if clubsListChanged:
	print("Writing " + clubsListRoot)
	clubsList.to_excel(clubsListRoot, index=False)
		
# Assign pupils to each club and write out a CSV file of members for each one.
changedClubMembers = {}
for clubName in clubMembers.keys():
	for clubIndex, clubValue in clubs.iterrows():
		if not clubValue["firstChildUsername"] == "" and clubValue["itemDescription"] == clubName:
			clubMembers[clubName].append(clubValue["firstChildUsername"])
		if not clubValue["secondChildUsername"] == "" and clubValue["itemDescription"] == clubName:
			clubMembers[clubName].append(clubValue["secondChildUsername"])
	csvPath = csvsRootStudents + os.sep + clubName + ".csv"
	if writeCSV(csvPath, "\n".join(clubMembers[clubName]).strip()):
		changedClubMembers[clubName] = clubMembers[clubName]

# For each club listed in the options sheet, make sure a matching Google Classroom exists and set teachers and pupil membership.
for clubsListIndex, clubsListValue in clubsList.iterrows():
	classroomID = ""
	for classroomIndex, classroomValue in classrooms.iterrows():
		if classroomValue["name"] == clubsListValue["club"]:
			classroomID = str(classroomValue["id"])
	if classroomID == "":
		os.system("gam create course name \"" + clubsListValue["club"] + "\" teacher " + clubsListValue["teacher"].split("\n")[0] + " status ACTIVE")
	else:
		csvPath = csvsRootTeachers + os.sep + clubsListValue["club"] + ".csv"
		if writeCSV(csvPath, "\n".join(teachers) + "\n" + clubsListValue["teacher"].replace(",","\n")):
			os.system("gam course " + classroomID + " sync teachers file \"" + csvPath + "\"")
		if clubsListValue["club"] in changedClubMembers.keys():
			os.system("gam course " + classroomID + " sync students file \"" + csvsRootStudents + os.sep + clubsListValue["club"] + ".csv\"")
