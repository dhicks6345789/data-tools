#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

# Set up yeargroups.
groupDetails = {
  "KS-SEC-PUPILS-NURSERY":{"Email":"nurserypupils@knightsbridgeschool.com","Form":"Lions"},
  "KS-SEC-PUPILS-RECEPTION":{"Email":"receptionpupils@knightsbridgeschool.com","Form":"Rec"},
  "KS-SEC-PUPILS-J1":{"Email":"j1pupils@knightsbridgeschool.com","Form":"1"},
  "KS-SEC-PUPILS-J2":{"Email":"j2pupils@knightsbridgeschool.com","Form":"2"},
  "KS-SEC-PUPILS-J3":{"Email":"j3pupils@knightsbridgeschool.com","Form":"3"},
  "KS-SEC-PUPILS-S4":{"Email":"s4pupils@knightsbridgeschool.com","Form":"4"},
  "KS-SEC-PUPILS-S5":{"Email":"s5pupils@knightsbridgeschool.com","Form":"5"},
  "KS-SEC-PUPILS-S6":{"Email":"s6pupils@knightsbridgeschool.com","Form":"6"},
  "KS-SEC-PUPILS-S7":{"Email":"s7pupils@knightsbridgeschool.com","Form":"7"},
  "KS-SEC-PUPILS-S8":{"Email":"s8pupils@knightsbridgeschool.com","Form":"8"}
}

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
  if not requiredConfigParameter in config.keys():
    print("Error - required value " + requiredConfigParameter + " not set in config.json.")
    sys.exit(1)

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,OldUsername,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output format: simply one user email address per line (yes, a valid CSV file), for use with GAM's import / sync function.

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Get a list of forms (excluding Nursery and Year 7 and 8, as they only have the one class).
forms={}
for pupilIndex, pupil in pupils.iterrows():
  for yearGroup in ["Rec","1","2","3","4","5","6","7"]:
    if yearGroup in pupil["Form"]:
      forms[pupil["Form"]] = 1

# Set up to create a CSV file for each form.
for form in forms.keys():
  groupDetails["KS-SEC-PUPILS-" + form] = {"Email":form + "pupils@knightsbridgeschool.com","Form":form}

# Create a CSV file for each group (i.e. Year Group or Form).
os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
for group in groupDetails.keys():
  print("Generating CSV file and syncing members for group " + group + " (" + groupDetails[group]["Email"].lower() + ")...")
  outputString = ""
  for pupilIndex, pupil in pupils.iterrows():
    if not re.match(".*" + groupDetails[group]["Form"] + ".*", pupil["Form"]) == None:
      outputString = outputString + pupil["OldUsername"] + "@knightsbridgeschool.com\n"
  installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv", outputString)
  os.system("gam update group " + groupDetails[group]["Email"].lower() + " sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv\" 2>&1")
	
# Read the existing basic staff details.
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)

outputString = ""
for staffIndex, staff in staff.iterrows():
  if not str(staff["Username"]) == "nan":
    outputString = outputString + str(staff["Username"]).lower() + "@knightsbridgeschool.com\n"
installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv", outputString)
os.system("gam update group staff@knightsbridgeschool.com sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv\" 2>&1")					
