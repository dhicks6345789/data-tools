#!/usr/bin/python
import os
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

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,OldUsername,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output format (for Google Groups upload):
# Group Email [Required],Member Email,Member Type,Member Role

for group in ["KS-SEC-PUPILS-S8"]:
  print(group)
  outputString = ""
  installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv", outputString)
  
#pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
#for pupilIndex, pupil in pupils.iterrows():
#	outputString = outputString + "P" + padString(str(pupil["ID"])) + "," + pupil["Username"] + ",Student,Library,OPAC Only,Pupils," + pupil["GivenName"] + "," + pupil["FamilyName"]+ "," + pupil["Form"]+ "," + str(pupil["DateOfBirth"]) + "\n"

#staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)
#for staffIndex, staff in staff.iterrows():
#	outputString = outputString + "S" + padString(str(staff["ID"])) + "," + str(staff["Username"]) + ",Staff,Library,Staff,Staff," + str(staff["GivenName"]) + "," + str(staff["FamilyName"]) + ",," + str(staff["DateOfBirth"]) + "\n"
	
#installLib.writeFile(config["dataFolder"] + os.sep + "Oliver" + os.sep + "allUsersForBorrowerImport.csv", outputString)
