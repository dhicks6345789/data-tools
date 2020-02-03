#!/usr/bin/python
import sys
import json
import pandas
import installLib

requiredConfigParameters = ["outputFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

# Output format:
# PupilID,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
pupils = pandas.DataFrame({"PupilID":[],"GivenName":[]})
installLib.writeFile(config["outputFolder"] + os.sep + "pupils.csv", pupils.to_csv())
