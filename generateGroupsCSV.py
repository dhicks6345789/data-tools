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
  "Nusery Pupils":{"Email":"nurserypupils@knightsbridgeschool.com","Form":"Lions"},
  "Reception Pupils":{"Email":"receptionpupils@knightsbridgeschool.com","Form":"Rec"},
  "J1 Pupils":{"Email":"j1pupils@knightsbridgeschool.com","Form":"1"},
  "J2 Pupils":{"Email":"j2pupils@knightsbridgeschool.com","Form":"2"},
  "J3 Pupils":{"Email":"j3pupils@knightsbridgeschool.com","Form":"3"},
  "S4 Pupils":{"Email":"s4pupils@knightsbridgeschool.com","Form":"4"},
  "S5 Pupils":{"Email":"s5pupils@knightsbridgeschool.com","Form":"5"},
  "S6 Pupils":{"Email":"s6pupils@knightsbridgeschool.com","Form":"6"},
  "S7 Pupils":{"Email":"s7pupils@knightsbridgeschool.com","Form":"7"},
  "S8 Pupils":{"Email":"s8pupils@knightsbridgeschool.com","Form":"8"}
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
  groupDetails[form + " Pupils"] = {"Email":form + "pupils@knightsbridgeschool.com","Form":form}

print groupDetails

sys.exit(0)

## Create a CSV file for each group (i.e. Year Group or Form).
#os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
#for group in groupDetails.keys():
#  print("Generating CSV file and syncing members for group " + group + " (" + groupDetails[group]["Email"].lower() + ")...")
#  outputString = ""
#  for pupilIndex, pupil in pupils.iterrows():
#    if not re.match(".*" + groupDetails[group]["Form"] + ".*", pupil["Form"]) == None:
#      outputString = outputString + pupil["OldUsername"] + "@knightsbridgeschool.com\n"
#  installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv", outputString)
#  os.system("gam update group " + groupDetails[group]["Email"].lower() + " sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv\" 2>&1")
	
## Read the existing basic staff details.
#staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)

#outputString = ""
#for staffIndex, staff in staff.iterrows():
#  if not str(staff["Username"]) == "nan":
#    outputString = outputString + str(staff["Username"]).lower() + "@knightsbridgeschool.com\n"
#installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv", outputString)
#os.system("gam update group staff@knightsbridgeschool.com sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv\" 2>&1")					
