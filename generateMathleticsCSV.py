#!/usr/bin/python
import os
import sys
import csv
import json
import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
outputRoot = config["dataFolder"] + os.sep + "GalorePark"
	
# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Example output:
# Action *,User ID,Type *,Username/Email *,Password,First name *,Middle name,Last name *,UPN,Access to application (Y/N) *
outputString = ""

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
for pupilIndex, pupil in pupils.iterrows():
	#outputString = outputString + "P" + padString(str(pupil["ID"])) + "," + pupil["Username"] + ",Student,Library,OPAC Only,Pupils," + pupil["GivenName"] + "," + pupil["FamilyName"]+ "," + pupil["Form"]+ "," + str(pupil["DateOfBirth"]) + "\n"
	outputString = outputString + "action," + str(pupil["ID"]) + ",Type," + pupil["Username"] + ",Password," + pupil["GivenName"] + ",," + pupil["FamilyName"] + ",UPN,Y"
installLib.writeFile(coutputRoot + os.sep + "galorePark.csv", outputString)
