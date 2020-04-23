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
outputRoot = config["dataFolder"] + os.sep + "Mathletics"
	
# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output in Excel spreadsheet:
# Student First Name (Mandatory), Student Surname (Mandatory), Student Year (Mandatory), Class Name (Mandatory), Teacher Title (Optional), Teacher First name (Mandatory), Teacher Surname (Mandatory), Teacher Email (Mandatory)
mathletics = pandas.DataFrame(columns=["Student First Name","Student Surname","Student Year","Class Name","Teacher Title","Teacher First name","Teacher Surname","Teacher Email"])

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
#for pupilIndex, pupil in pupils.iterrows():
#	outputString = outputString + "action," + str(pupil["ID"]) + ",Type," + pupil["Username"] + ",Password," + pupil["GivenName"] + ",," + pupil["FamilyName"] + ",UPN,Y"

mathletics.to_excel(outputRoot, index=False)
