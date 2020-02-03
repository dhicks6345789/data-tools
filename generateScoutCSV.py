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

# Input:
#Date,person_id,UserName,Forename,Surname,PreferredForename,PreferredSurname,Password,RegistrationGroup,Year,DOB
#2020-01-27,,a.astudent16,AaSal,astudent,AaSal,aStudent,KS160311!,S4L,4,16/03/2011

# Output: P1949,ksbsmith5,Student,Library,OPAC Only,Pupils,Bob,Smith,S5C,28/01/2014

pupils = open(config["pupilsCSVInputFile"])
pupilsReader = csv.reader(pupils, delimiter=',')
for pupilRow in pupilsReader:
	print(pupilRow[0] + "," + pupilRow[6].split("@")[0] + ",Student,Library,OPAC Only,Pupils," + pupilRow[2] + "," + pupilRow[4] + "," + pupilRow[5])