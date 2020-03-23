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
    outputString = outputString + pupil["OldUsername"] + "@knightsbridgeschool.com\n"
    
print(outputString)

# Set up to create a CSV file for each form.
#for form in forms.keys():
#  groupDetails["KS-SEC-PUPILS-" + form] = {"Email":form + "pupils@knightsbridgeschool.com","Form":form}

# Create a CSV file for each group (i.e. Year Group or Form).
#os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
#for group in groupDetails.keys():
#  print("Generating CSV file and syncing members for group " + group + " (" + groupDetails[group]["Email"].lower() + ")...")
#  outputString = ""
#  for pupilIndex, pupil in pupils.iterrows():
#    if not re.match(".*" + groupDetails[group]["Form"] + ".*", pupil["Form"]) == None:
#      outputString = outputString + pupil["OldUsername"] + "@knightsbridgeschool.com\n"
#  installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv", outputString)
#  os.system("gam update group " + groupDetails[group]["Email"].lower() + " sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv\" 2>&1")
