#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

yearNames = {"Year 1":"J1","Year 2":"J2","Year 3":"J3","Year 4":"S4","Year 5":"S5","Year 6":"S6","Year 7":"S7","Year 8":"S8","Yr 1":"J1","Yr 2":"J2","Yr 3":"J3","Yr 4":"S4","Yr 5":"S5","Yr 6":"S6","Yr 7":"S7","Yr 8":"S8"}
def normaliseYearNames(theString):
  for wrongString in yearNames.keys():
    theString = re.sub(".*" + wrongString + ".*", yearNames[wrongString], theString)
  return(theString)

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

unHandledCourses = []
for courseIndex, course in courses.iterrows():
  if course["courseState"] == "ACTIVE":
    formFound = False
    for form in forms:
      if form in normaliseYearNames(course["name"]):
        formFound = True
        print("Assign " + form + " to " + course["name"])
    if formFound == False:
      unHandledCourses.append(course["name"])

print("Unhandled courses:")
print(unHandledCourses)
#installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv", outputString)
