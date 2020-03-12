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

# Input data headings:
# id,name,courseState,descriptionHeading,description,section,room,enrollmentCode,guardiansEnabled,alternateLink,ownerId,creationTime,updateTime,calendarId,courseGroupEmail,teacherGroupEmail,teacherFolder.id,teacherFolder.title,teacherFolder.alternateLink,courseMaterialSets,courseMaterialSets.0.materials.0.driveFile.alternateLink,courseMaterialSets.0.materials.0.driveFile.id,courseMaterialSets.0.materials.0.driveFile.title,courseMaterialSets.0.title

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Get a list of forms (excluding Nursery and Year 7 and 8, as they only have the one class).
forms={}
for pupilIndex, pupil in pupils.iterrows():
  for yearGroup in ["Rec","1","2","3","4","5","6","7","8"]:
    if yearGroup in pupil["Form"]:
      forms[pupil["Form"]] = 1

print(forms.keys())
      
#installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv", outputString)
