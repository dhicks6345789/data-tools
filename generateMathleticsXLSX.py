#!/usr/bin/python
import os
import sys
import csv
import json
import pandas
import dataLib

validYeargroups = ["Rec","J1","J2","J3","S4"]

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
mathletics = pandas.DataFrame(columns=["Student First Name","Student Surname","Student Year","Class Name","Teacher Title","Teacher First name","Teacher Surname","Teacher Email"])

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
for pupilsIndex, pupilsValues in pupils.iterrows():
	pupilValid = False
	for validYeargroup in validYeargroups:
		if validYeargroup in pupilsValues["Form"]:
			pupilValid = True
	if pupilValid:
		mathletics.at[pupilsIndex+1, "Student First Name"] = pupilsValues["GivenName"]
		mathletics.at[pupilsIndex+1, "Student Surname"] = pupilsValues["FamilyName"]
		mathletics.at[pupilsIndex+1, "Student Year"] = pupilsValues["YearGroup"]
		mathletics.at[pupilsIndex+1, "Class Name"] = pupilsValues["Form"]
		#mathletics.at[pupilsIndex+1, "Teacher Title"] = pupilsValues[""]
		#mathletics.at[pupilsIndex+1, "Teacher First Name"] = pupilsValues[""]
		#mathletics.at[pupilsIndex+1, "Teacher Surname"] = pupilsValues[""]
		#mathletics.at[pupilsIndex+1, "Teacher Email"] = pupilsValues[""]

mathletics.to_excel(outputRoot + os.sep + "Mathletics.xlsx", index=False)
