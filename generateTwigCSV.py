#!/usr/bin/python
import os
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

def shortenGUID(theGUID):
	theGUID = theGUID.replace("-","")
	result = ""
	for pl in [0,4,8,12,16,20,24,28]:
		result = result + theGUID[pl]
	return(result)

def padString(theString):
	result = theString
	for pl in range(0, 8 - len(theString)):
		result = "0" + result
	return result
	
# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

# Make sure the output folder exists.
os.makedirs(config["dataFolder"] + os.sep + "Twig", exist_ok=True)

# Pupils, input: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Pupils, output: Unique ID (optional),Teacher Name (required),Email (required),Class (optional),Student Group (optional),Password (required),Username (optional)
outputString = "Unique ID,Student Name,Email,Class,Student Group,Password,Username\n"
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
for pupilIndex, pupil in pupils.iterrows():
	outputString = outputString + "P" + padString(str(pupil["ID"])) + "," + pupil["GivenName"] + " " + pupil["FamilyName"] + "," + pupil["OldUsername"] + "@knightsbridgeschool.com," + pupil["Form"] + ",,,\n"
installLib.writeFile(config["dataFolder"] + os.sep + "Twig" + os.sep + "pupils.csv", outputString)

# Staff, input: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Staff, output: Unique ID (optional),Teacher Name (required),Email (required),Class (optional),Student Group (optional),Password (required),Username (optional)
outputString = "Unique ID,Teacher Name,Email,Class,Student Group,Password,Username\n"
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)
for staffIndex, staff in staff.iterrows():
	outputString = outputString + "S" + padString(str(staff["ID"])) + "," + staff["GivenName"] + " " + staff["FamilyName"] + "," + staff["Username"] + "@knightsbridgeschool.com,,,,\n"
installLib.writeFile(config["dataFolder"] + os.sep + "Twig" + os.sep + "staff.csv", outputString)
