#!/usr/bin/python
import sys
import csv
import json
import installLib

requiredConfigParameters = ["pupilsCSVInputFile", "outputFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

print(config["pupilsCSVInputFile"])
print(config["outputFolder"] + "\\Scout\\allUsersForBorrowerImport.csv")

# Orig: P1949,kskirkoli15,Student,Library,OPAC Only,Pupils,Olivia,Kirkup,S5C,28/01/2009

#'person_id', 'person_number', 'first_name', 'middle_name', 'last_name', 'grade_level', 'email_address', 'sis_username', 'password_policy', 'location_id'
#'104', '104', 'Timothy', '', 'Nasser', 'S4L', 't.nasser16@knightsbridgeschool.com', '104', '4', 'KnightsbridgeSchool'

pupils = open(config["pupilsCSVInputFile"])
pupilsReader = csv.reader(pupils, delimiter=',')
for pupilRow in pupilsReader:
	print(pupilRow["person_id"] + "," + pupilRow[""] + "Student,Library,OPAC Only,Pupils," + pupilRow["first_name"] + "," + pupilRow["last_name"] + "," + pupilRow["grade_level"])
