#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

# Set up the initial set of groups - one per yeargroup.
groupDetails = {
	"Nusery Pupils":{"email":"nurserypupils@knightsbridgeschool.com","group":"Lions"},
	"Reception Pupils":{"email":"receptionpupils@knightsbridgeschool.com","group":"Rec"},
	"J1 Pupils":{"email":"j1pupils@knightsbridgeschool.com","group":"J1"},
	"J2 Pupils":{"email":"j2pupils@knightsbridgeschool.com","group":"J2"},
	"J3 Pupils":{"email":"j3pupils@knightsbridgeschool.com","group":"J3"},
	"S4 Pupils":{"email":"s4pupils@knightsbridgeschool.com","group":"S4"},
	"S5 Pupils":{"email":"s5pupils@knightsbridgeschool.com","group":"S5"},
	"S6 Pupils":{"email":"s6pupils@knightsbridgeschool.com","group":"S6"},
	"S7 Pupils":{"email":"s7pupils@knightsbridgeschool.com","group":"S7"},
	"S8 Pupils":{"email":"s8pupils@knightsbridgeschool.com","group":"S8"}
}

# Get a list of yeargroups.
yeargroups = []
for group in groupDetails.keys():
	yeargroups.append(groupDetails[group]["group"])
installLib.writeFile(config["dataFolder"] + os.sep + "yeargroups.csv", sorted(yeargroups.keys()))

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

# Get a list of forms - a "form" here is any sub-yeargroup sized group of pupils, we skip any forms which are simply a whole yeargroup.
forms = {}
for pupilIndex, pupil in pupils.iterrows():
	form = pupil["Form"]
	if not form in yeargroups:
		forms[form] = 1

# Add the list of forms to groupDetails.
for form in forms.keys():
	groupDetails[form + " Pupils"] = {"email":form + "pupils@knightsbridgeschool.com","group":form}

# Add the members of each pupil group.
for group in groupDetails.keys():
	groupDetails[group]["Members"] = []
	for pupilIndex, pupil in pupils.iterrows():
		if groupDetails[group]["group"] in pupil["Form"]:
			groupDetails[group]["Members"].append(pupil["OldUsername"] + "@knightsbridgeschool.com")

# Create a CSV file for each group (i.e. Year Group or Form).
allPupils = ""
os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
for group in groupDetails.keys():
	outputString = ""
	for member in groupDetails[group]["Members"]:
		outputString = outputString + member + "\n"
		allPupils = allPupils + member + "\n"
	installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv", outputString)
	print("Sync group " + group + " from CSV to GSuite.")
	os.system("gam update group " + groupDetails[group]["email"].lower() + " name \"" + group + "\" 2>&1")
	os.system("gam update group " + groupDetails[group]["email"].lower() + " sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv\" 2>&1")
	
# Write out the All Pupils CSV file.
installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "Pupils.csv", allPupils)
os.system("gam update group pupils@knightsbridgeschool.com name pupils 2>&1")
os.system("gam update group pupils@knightsbridgeschool.com sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + "Pupils.csv\" 2>&1")
	
# Read the existing basic staff details.
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)

outputString = ""
for staffIndex, staff in staff.iterrows():
	if not str(staff["Username"]) == "nan":
		outputString = outputString + str(staff["Username"]).lower() + "@knightsbridgeschool.com\n"
installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "Staff.csv", outputString)
print("Sync group Staff from CSV to GSuite.")
os.system("gam update group staff@knightsbridgeschool.com sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + "Staff.csv\" 2>&1")					
