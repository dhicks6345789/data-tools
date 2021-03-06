#!/usr/bin/python
import os
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

def shortenGUID(theGUID):
	theGUID = theGUID.replace("-","")
	result = ""
	for pl in [0,4,8,12,16,20,24,28]:
		result = result + theGUID[pl]
	return(result)

def padString(theString):
	result = theString
	for pl in range(0, 8 - len(theString)):
		result = "0" + result
	return result
	
# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# 2020-01-27,,a.astudent16,AaSal,astudent,AaSal,aStudent,kfkbhrg!,S4L,4,16/03/2011
# Example output:
# Pupils: P1949,ksbsmith15,Student,Library,OPAC Only,Pupils,Bob,Smith,S5C,xx/yy/zzzz
# Staff: S145,b.smith,Staff,Library,Staff,Staff,Bob,Smith,,xx/yy/zzzz
outputString = ""

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
for pupilIndex, pupil in pupils.iterrows():
	outputString = outputString + "P" + padString(str(pupil["ID"])) + "," + pupil["Username"] + ",Student,Library,OPAC Only,Pupils," + pupil["GivenName"] + "," + pupil["FamilyName"]+ "," + pupil["Form"]+ "," + str(pupil["DateOfBirth"]) + "\n"

staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)
for staffIndex, staff in staff.iterrows():
	outputString = outputString + "S" + padString(str(staff["ID"])) + "," + str(staff["Username"]) + ",Staff,Library,Staff,Staff," + str(staff["GivenName"]) + "," + str(staff["FamilyName"]) + ",," + str(staff["DateOfBirth"]) + "\n"
	
installLib.writeFile(config["dataFolder"] + os.sep + "Oliver" + os.sep + "allUsersForBorrowerImport.csv", outputString)
