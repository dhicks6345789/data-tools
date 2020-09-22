#!/usr/bin/python
import os
import sys
import json
import pandas
import dataLib

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

for staffIndex, staffValues in teachers.iterrows():
	cpoms.at[staffIndex+1, "Firstname"] = staffValues["GivenName"]
	cpoms.at[staffIndex+1, "Surname"] = staffValues["FamilyName"]
	cpoms.at[staffIndex+1, "School/Establishment Email Address"] = staffValues["Username"] + "@knightsbridgeschool.com"
		
cpoms.to_excel(outputRoot + os.sep + "CPOMS.xlsx", index=False)
