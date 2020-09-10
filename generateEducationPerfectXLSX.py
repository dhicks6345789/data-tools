#!/usr/bin/python
import os
import sys
import csv
import json
import pandas
import dataLib

validYeargroups = ["5","6","7","8","9"]

def formToYearGroup(theForm):
	for validYeargroup in validYeargroups:
		if validYeargroup in theForm:
			return validYeargroup.replace("Rec","R")
	return None

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
outputRoot = config["dataFolder"] + os.sep + "EducationPerfect"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor,Contacts
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output in Excel spreadsheet:
# First Name,Surname,Class Name,Teacher Name/s,Student ID,Student Email Address,SSO Identifier,Parent Email Address (optional)
perfect = pandas.DataFrame(columns=["First Name","Surname","Class Name","Teacher Name/s","Student ID","Student Email Address","SSO Identifier","Parent Email Address"])

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
teachers = pandas.read_excel(outputRoot + os.sep + "Teachers.xlsx", header=0)
for pupilsIndex, pupilsValues in pupils.iterrows():
	yearGroup = formToYearGroup(pupilsValues["Form"])
	if not yearGroup == None:
		perfect.at[pupilsIndex+1, "First Name"] = pupilsValues["GivenName"]
		perfect.at[pupilsIndex+1, "Surname"] = pupilsValues["FamilyName"]
		perfect.at[pupilsIndex+1, "Class Name"] = pupilsValues["Form"]
		#for teachersIndex, teachersValues in teachers.iterrows():
		#	if pupilsValues["Form"] == teachersValues["Class Name"]:
		#		perfect.at[pupilsIndex+1, "Teacher Name/s"] = teachersValues["Teacher First name"] + " " + teachersValues["Teacher Surname"]
		perfect.at[pupilsIndex+1, "Student ID"] = pupilsValues["GUID"]
		perfect.at[pupilsIndex+1, "Student Email Address"] = pupilsValues["Username"] + "@knightsbridgeschool.com"
		perfect.at[pupilsIndex+1, "SSO Identifier"] = pupilsValues["Username"] + "@knightsbridgeschool.com"
		perfect.at[pupilsIndex+1, "Parent Email Address"] = pupilsValues["Contacts"].split(",")[0]

perfect.to_excel(outputRoot + os.sep + "EducationPerfect.xlsx", index=False)
