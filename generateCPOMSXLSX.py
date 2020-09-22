#!/usr/bin/python
import os
import sys
import json
import pandas
import dataLib

def cellToStr(theInput):
	if type(theInput) == "string":
		return(theInput)
	return(str(theInput))

groups = {
	"Teacher":["teacher", "head"],
	"TA":["teaching assistant","classroom assistant","gap student"]
}

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
outputRoot = config["dataFolder"] + os.sep + "CPOMS"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output in Excel spreadsheet:
cpoms = pandas.DataFrame(columns=["Firstname","Surname","School/Establishment Email Address","Job Title","User Group","Class Restrictions"])
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)

for staffIndex, staffValues in staff.iterrows():
	cpoms.at[staffIndex+1, "Firstname"] = staffValues["GivenName"]
	cpoms.at[staffIndex+1, "Surname"] = staffValues["FamilyName"]
	cpoms.at[staffIndex+1, "School/Establishment Email Address"] = staffValues["Username"] + "@knightsbridgeschool.com"
	cpoms.at[staffIndex+1, "Job Title"] = staffValues["JobTitle"]
	for groupTitle in groups.keys():
		for keyword in groups[groupTitle]:
			if keyword in cellToStr(staffValues["JobTitle"]).lower():
				cpoms.at[staffIndex+1, "User Group"] = groupTitle
		
cpoms.to_excel(outputRoot + os.sep + "CPOMS.xlsx", index=False)
