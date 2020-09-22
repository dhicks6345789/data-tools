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
outputRoot = config["dataFolder"] + os.sep + "CPOMS"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output in Excel spreadsheet:
cpoms = pandas.DataFrame(columns=["Firstname","Surname","School/Establishment Email Address","Job Title","User Group","Class Restrictions"])
teachers = pandas.read_excel(outputRoot + os.sep + "Teachers.xlsx", header=0)
for teachersIndex, teachersValues in teachers.iterrows():
	cpoms.at[teachersIndex+1, "Firstname"] = teachersValues["GivenName"]
	cpoms.at[teachersIndex+1, "Surname"] = teachersValues["FamilyName"]
	cpoms.at[teachersIndex+1, "School/Establishment Email Address"] = teachersValues["Username"] + "@knightsbridgeschool.com"
		
mathletics.to_excel(outputRoot + os.sep + "CPOMS.xlsx", index=False)
