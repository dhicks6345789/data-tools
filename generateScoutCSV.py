#!/usr/bin/python
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["pupilsCSVInputFile", "outputFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

# Input data headings:
# Date,person_id,UserName,Forename,Surname,PreferredForename,PreferredSurname,Password,RegistrationGroup,Year,DOB
# 2020-01-27,,a.astudent16,AaSal,astudent,AaSal,aStudent,kfkbhrg!,S4L,4,16/03/2011
# Example output:
# P1949,ksbsmith5,Student,Library,OPAC Only,Pupils,Bob,Smith,S5C,28/01/2014
pupils = pandas.read_csv(config["pupilsCSVInputFile"], header=0)
for pupilIndex, pupil in pupils.iterrows():
	print(str(pupil["person_id"]) + "," + pupil["UserName"] + ",Student,Library,OPAC Only,Pupils," + pupil["PreferredForename"] + "," + pupil["PreferredSurname"]+ "," + pupil["RegistrationGroup"]+ "," + str(pupil["DOB"]))
