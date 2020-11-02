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

# Make sure the output folder exists.
os.makedirs(config["dataFolder"] + os.sep + "Bebras", exist_ok=True)

# Pupils, input: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Pupils, output: Class, Grade (English), Firstname, Lastname, Password, Gender
outputString = "Class,Grade (English),Firstname,Lastname,Password,Gender\n"
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
for pupilIndex, pupil in pupils.iterrows():
	pupilPassword = ""
	outputString = outputString + pupil["Form"] + "," + str(pupil["YearGroup"]) + "," + pupil["GivenName"] + " " + pupil["FamilyName"] + "," + pupilPassword + "," + pupil["Gender"] + "\n"
installLib.writeFile(config["dataFolder"] + os.sep + "Bebras" + os.sep + "pupils.csv", outputString)