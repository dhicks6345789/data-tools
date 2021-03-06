#!/usr/bin/python
import os
import sys
import json
import pandas
import dataLib

parentEmailYeargroups = ["3","4"]
ownEmailYearGroups = ["5","6","7","8"]

def formToYearGroup(theForm):
	for validYeargroup in parentEmailYeargroups + ownEmailYearGroups:
		if validYeargroup in theForm:
			return validYeargroup.replace("Rec","R")
	return None

yearGroupToLevel = {"3":"1","4":"1","5":"2","6":"2","7":"3","8":"3"}

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
outputRoot = config["dataFolder"] + os.sep + "FirstNews"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Output in CSV format:
# First Name,Last Name,"Level (1, 2 or 3)",Parent/Student Email
# Delete,Me,1,pupil@exampleemail.com

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

forms = {}
for pupilsIndex, pupilsValues in pupils.iterrows():
	forms[pupilsValues["Form"]] = 1

for form in forms.keys():
	yearGroup = formToYearGroup(form)
	if not yearGroup == None:
		firstNews = pandas.DataFrame(columns=["First Name","Last Name","Level","Email"])
		for pupilsIndex, pupilsValues in pupils.iterrows():
			if pupilsValues["Form"] == form:
				firstNews.at[pupilsIndex+1, "First Name"] = pupilsValues["GivenName"]
				firstNews.at[pupilsIndex+1, "Last Name"] = pupilsValues["FamilyName"]
				firstNews.at[pupilsIndex+1, "Level"] = yearGroupToLevel[yearGroup]
				if yearGroup in ownEmailYearGroups:
					firstNews.at[pupilsIndex+1, "Email"] = pupilsValues["OldUsername"] + "@knightsbridgeschool.com"
				else:
					firstNews.at[pupilsIndex+1, "Email"] = pupilsValues["Contacts"].split(" ")[0]
		firstNews.to_csv(outputRoot + os.sep + form + ".csv", index=False)
