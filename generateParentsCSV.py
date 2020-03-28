#!/usr/bin/python
import os
import re
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

def readFile(theFilename):
	inHandle = open(theFilename)
	inData = inHandle.read()
	inHandle.close()
	return inData

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,OldUsername,YearGroup,Form,Tutor

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

groups = []
for yeargroup in readFile(config["dataFolder"] + os.sep + "yeargroups.csv").split("\n"):
	if not yeargroup == "" and not yeargroup in groups:
		groups.append(yeargroup)
for form in readFile(config["dataFolder"] + os.sep + "forms.csv").split("\n"):
	if not form == "" and not form in groups:
		groups.append(form)

os.makedirs(config["dataFolder"] + os.sep + "Parents", exist_ok=True)
for group in groups:
	groupMembers = []
	for pupilIndex, pupil in pupils.iterrows():
		if group in pupil["Form"]:
			groupMembers.append(pupil["MainContact"])
	installLib.writeFile(config["dataFolder"] + os.sep + "Parents" + os.sep + group + ".csv", groupMembers)
