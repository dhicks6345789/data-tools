#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]
groupDetails = {"KS-SEC-PUPILS-S8":{"Email":"s8pupils@knightsbridgeschool.com","Form":"8"}}

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

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
for group in groupDetails.keys():
  print(group)
  outputString = "Group Email [Required],Member Email [Required],Member Type,Member Role\n"
  for pupilIndex, pupil in pupils.iterrows():
    if not re.match(".*" + groupDetails[group]["Form"] + ".*", pupil["Form"]) == None:
      outputString = outputString + groupDetails[group]["Email"] + "," + pupil["OldUsername"] + "@knightsbridgeschool.com,USER,MEMBER\n"
  installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv", outputString)
	
#staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)
#for staffIndex, staff in staff.iterrows():
#. outputString = outputString + "S" + padString(str(staff["ID"])) + "," + str(staff["Username"]) + ",Staff,Library,Staff,Staff," + str(staff["GivenName"]) + "," + str(staff["FamilyName"]) + ",," + str(staff["DateOfBirth"]) + "\n"
