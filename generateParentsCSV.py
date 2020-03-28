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

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,OldUsername,YearGroup,Form,Tutor

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

yeargroups = str(installLib.readFile(config["dataFolder"] + os.sep + "yeargroups.csv")).split("\n")
forms = str(installLib.readFile(config["dataFolder"] + os.sep + "forms.csv")).split("\n")
for group in yeargroups + forms:
	print(group)
	
#for pupilIndex, pupil in pupils.iterrows():
#	print(pupil["Username"])
