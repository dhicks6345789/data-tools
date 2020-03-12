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

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Get a list of years and forms.
forms={"NUSERY":1,"RECEPTION":1,"J1":1,"J2":1,"J3":1,"S4":1,"S5":1,"S6":1,"S7":1,"S8":1}
for pupilIndex, pupil in pupils.iterrows():
  forms[pupil["Form"]] = 1  
forms = forms.keys()

print(forms)

# Read the Courses list. Courses CSV headings:
# id,name,courseState,descriptionHeading,description,section,room,enrollmentCode,guardiansEnabled,alternateLink,ownerId,creationTime,updateTime,calendarId,courseGroupEmail,teacherGroupEmail,teacherFolder.id,teacherFolder.title,teacherFolder.alternateLink,courseMaterialSets,courseMaterialSets.0.materials.0.driveFile.alternateLink,courseMaterialSets.0.materials.0.driveFile.id,courseMaterialSets.0.materials.0.driveFile.title,courseMaterialSets.0.title
courses = pandas.read_csv(config["dataFolder"] + os.sep + "courses.csv", header=0)

for courseIndex, course in courses.iterrows():
  if course["courseState"] == "ACTIVE"
    print(course["name"])

#installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv", outputString)
