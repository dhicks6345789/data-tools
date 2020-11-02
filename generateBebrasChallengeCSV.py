#!/usr/bin/python
import os
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

validYeargroups = ["S5","S6","S7","S8","S9"]
	
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
	for validYeargroup in validYeargroups:
		if validYeargroup in pupil["Form"]:
			outputString = outputString + pupil["Form"] + "," + pupil["Form"][1] + "," + pupil["GivenName"] + "," + pupil["FamilyName"] + "," + pupil["Password"] + "," + pupil["Gender"] + "\n"
installLib.writeFile(config["dataFolder"] + os.sep + "Bebras" + os.sep + "bebras.csv", outputString)
