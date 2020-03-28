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

# Read the contens of a file.
def readFile(theFilename):
	inHandle = open(theFilename)
	inData = inHandle.read()
	inHandle.close()
	return inData

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Read the Forms and Yeargroups into one list.
classGroups = []
for yeargroup in readFile(config["dataFolder"] + os.sep + "yeargroups.csv").split("\n"):
	if not yeargroup == "" and not yeargroup in classGroups:
		classGroups.append(yeargroup)
for form in readFile(config["dataFolder"] + os.sep + "forms.csv").split("\n"):
	if not form == "" and not form in classGroups:
		classGroups.append(form)

os.makedirs(config["dataFolder"] + os.sep + "DefaultPupilPasswords", exist_ok=True)
for pupilIndex, pupil in pupils.iterrows():
	print(pupil["OldUsername"])

print(classGroups)
