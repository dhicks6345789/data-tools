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

# Output format: CSV file with header row -  First Name,Last Name,Student ID,Grade,Email Address

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

print("Generating CSV files ready for upload to Typing Club's system.")

# Generate the allUsers.csv file.
outputString = "First Name,Last Name,Student ID,Grade,Email Address\n"
for pupilIndex, pupil in pupils.iterrows():
    outputString = outputString + pupil["GivenName"] + "," + pupil["FamilyName"] + ",P" + str(pupil["ID"]) + "," + str(20 - pupil["YearGroup"]) + "," + pupil["OldUsername"] + "@knightsbridgeschool.com\n"
    
installLib.writeFile(config["dataFolder"] + os.sep + "TypingClub" + os.sep + "allUsers.csv", outputString)

# Get a list of forms from the basic pupil data.
forms={}
for pupilIndex, pupil in pupils.iterrows():
  forms[pupil["Form"]] = 1

# Set up to create a CSV file for each form.
for form in forms.keys():
  outputString = "First Name,Last Name,Student ID,Grade,Email Address\n"
  for pupilIndex, pupil in pupils.iterrows():
    if pupil["Form"] == form:
      outputString = outputString + pupil["GivenName"] + "," + pupil["FamilyName"] + ",P" + str(pupil["ID"]) + "," + str(20 - pupil["YearGroup"]) + "," + pupil["OldUsername"] + "@knightsbridgeschool.com\n"
  installLib.writeFile(config["dataFolder"] + os.sep + "TypingClub" + os.sep + form + ".csv", outputString)
  
