#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

def readFile(theFilename):
	inHandle = open(theFilename)
	inData = inHandle.read()
	inHandle.close()
	return inData

def multisplit(theString, theSplit):
	result = theString.split(theSplit[0])
	for pl in range(1, len(theSplit)):
		tempResult = result
		for resultItem in result:
			for splitItem in resultItem.split(theSplit[pl]):
				tempResult.append(splitItem)
		result = tempResult
	return result

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,OldUsername,YearGroup,Form,Tutor

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

classGroups = []
for yeargroup in readFile(config["dataFolder"] + os.sep + "yeargroups.csv").split("\n"):
	if not yeargroup == "" and not yeargroup in classGroups:
		classGroups.append(yeargroup)
for form in readFile(config["dataFolder"] + os.sep + "forms.csv").split("\n"):
	if not form == "" and not form in classGroups:
		classGroups.append(form)
		
# Read the existing (GSuite) groups data.
groupEmails = []
groups = pandas.read_csv(config["dataFolder"] + os.sep + "groups.csv", header=0)
for groupIndex, group in groups.iterrows():
	groupEmails.append(groups.at[groupIndex, "email"])

print(multisplit("abc;def ghi", " ;"))
sys.exit(0)
	
os.makedirs(config["dataFolder"] + os.sep + "Parents" + os.sep + "ByClassOrYearGroup", exist_ok=True)
for classGroup in classGroups:
	groupMembers = []
	for pupilIndex, pupil in pupils.iterrows():
		if classGroup in pupil["Form"]:
			if not str(pupil["Contacts"]) == "nan":
				for contact in str(pupil["Contacts"]).split():
					groupMembers.append(contact)
	installLib.writeFile(config["dataFolder"] + os.sep + "Parents" + os.sep + "ByClassOrYearGroup" + os.sep + classGroup + ".csv", groupMembers)
	groupEmail = classGroup.lower() + "parents@knightsbridgeschool.com"
	if not groupEmail in groupEmails:
		os.system("gam create group " + groupEmail + " name \"" + classGroup + " Parents\" description \"Parents of " + classGroup + "\" 2>&1")
	os.system("gam update group " + groupEmail + " sync member file \"" + config["dataFolder"] + os.sep + "Parents" + os.sep + "ByClassOrYearGroup" + os.sep + classGroup + ".csv\" 2>&1")

os.makedirs(config["dataFolder"] + os.sep + "Parents" + os.sep + "Guardians", exist_ok=True)
for classGroup in classGroups:
	CSVString = "ID,Name,Username,OldUsername,Guardian\n"
	for pupilIndex, pupil in pupils.iterrows():
		if classGroup in pupil["Form"]:
			if not str(pupil["Contacts"]) == "nan":
				for contact in str(pupil["Contacts"]).split():
					CSVString = CSVString + str(pupil["ID"]) + "," + pupil["GivenName"] + " " + pupil["FamilyName"] + "," + pupil["Username"] + "," + pupil["OldUsername"] + "," + contact + "\n"
	installLib.writeFile(config["dataFolder"] + os.sep + "Parents" + os.sep + "Guardians" + os.sep + classGroup + ".csv", CSVString)
