#!/usr/bin/python
import os
import sys
import csv
import json
import pandas
import dataLib

validYeargroups = ["Rec","1","2","3","4"]

def formToYearGroup(theForm):
	for validYeargroup in validYeargroups:
		if validYeargroup in theForm:
			return validYeargroup.replace("Rec","R")
	return None

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
outputRoot = config["dataFolder"] + os.sep + "Mathletics"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output in Excel spreadsheet:
# Student First Name (Mandatory), Student Surname (Mandatory), Student Year (Mandatory), Class Name (Mandatory), Teacher Title (Optional), Teacher First name (Mandatory), Teacher Surname (Mandatory), Teacher Email (Mandatory)
mathletics = pandas.DataFrame(columns=["Student First Name (Mandatory)","Student Surname (Mandatory)","Student Year (Mandatory)","Class Name (Mandatory)","Teacher Title (Optional)","Teacher First name (Mandatory)","Teacher Surname (Mandatory)","Teacher Email (Mandatory)"])
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
students = pandas.read_excel(outputRoot + os.sep + "Students.xlsx", header=0)
teachers = pandas.read_excel(outputRoot + os.sep + "Teachers.xlsx", header=0)
for pupilsIndex, pupilsValues in pupils.iterrows():
	yearGroup = formToYearGroup(pupilsValues["Form"])
	if not yearGroup == None:
		studentFound = False
		for studentsIndex, studentsValues in students.iterrows():
			if studentsValues["Student First Name (Mandatory)"] == pupilsValues["GivenName"] and studentsValues["Student Surname (Mandatory)"] == pupilsValues["FamilyName"]:
				studentFound = True
				mathletics.at[pupilsIndex+1, "Student First Name (Mandatory)"] = studentsValues["Student First Name (Mandatory)"]
				mathletics.at[pupilsIndex+1, "Student Surname (Mandatory)"] = studentsValues["Student Surname (Mandatory)"]
				mathletics.at[pupilsIndex+1, "Student Year (Mandatory)"] = yearGroup
				mathletics.at[pupilsIndex+1, "Class Name (Mandatory)"] = studentsValues["Class Name (Mandatory)"]
				mathletics.at[pupilsIndex+1, "Teacher Title (Optional)"] = studentsValues["Teacher Title (Optional)"]
				mathletics.at[pupilsIndex+1, "Teacher First name (Mandatory)"] = studentsValues["Teacher First name (Mandatory)"]
				mathletics.at[pupilsIndex+1, "Teacher Surname (Mandatory)"] = studentsValues["Teacher Surname (Mandatory)"]
				mathletics.at[pupilsIndex+1, "Teacher Email (Mandatory)"] = studentsValues["Teacher Email (Mandatory)"]
		if not studentFound:
			mathletics.at[pupilsIndex+1, "Student First Name (Mandatory)"] = pupilsValues["GivenName"]
			mathletics.at[pupilsIndex+1, "Student Surname (Mandatory)"] = pupilsValues["FamilyName"]
			mathletics.at[pupilsIndex+1, "Student Year (Mandatory)"] = yearGroup
			mathletics.at[pupilsIndex+1, "Class Name (Mandatory)"] = pupilsValues["Form"]
			for teachersIndex, teachersValues in teachers.iterrows():
				if pupilsValues["Form"] == teachersValues["Class Name"]:
					mathletics.at[pupilsIndex+1, "Teacher Title (Optional)"] = teachersValues["Teacher Title"]
					mathletics.at[pupilsIndex+1, "Teacher First name (Mandatory)"] = teachersValues["Teacher First name"]
					mathletics.at[pupilsIndex+1, "Teacher Surname (Mandatory)"] = teachersValues["Teacher Surname"]
					mathletics.at[pupilsIndex+1, "Teacher Email (Mandatory)"] = teachersValues["Teacher Email"]

mathletics.to_excel(outputRoot + os.sep + "Mathletics.xlsx", index=False)
