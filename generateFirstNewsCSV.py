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

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
outputRoot = config["dataFolder"] + os.sep + "FirstNews"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output in CSV format:
# First Name,Last Name,"Level (1, 2 or 3)",Parent/Student Email
# Delete,Me,1,pupil@exampleemail.com
firstNews = pandas.DataFrame(columns=["First Name","Last Name","Level","Email"])

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

for pupilsIndex, pupilsValues in pupils.iterrows():
	yearGroup = formToYearGroup(pupilsValues["Form"])
	if not yearGroup == None:
		firstNews.at[pupilsIndex+1, "First Name"] = pupilsValues["GivenName"]

firstNews.to_csv(outputRoot + os.sep + "FirstNews.csv", index=False)
