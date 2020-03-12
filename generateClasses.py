#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

yearNames = {"Year 1":"J1","Year 2":"J2","Year 3":"J3","Year 4":"S4","Year 5":"S5","Year 6":"S6","Year 7":"S7","Year 8":"S8","Yr 1":"J1","Yr 2":"J2","Yr 3":"J3","Yr 4":"S4","Yr 5":"S5","Yr 6":"S6","Yr 7":"S7","Yr 8":"S8","Y1":"J1","Y2":"J2","Y3":"J3","Y4":"S4","Y5":"S5","Y6":"S6","Y7":"S7","Y8":"S8"}
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
    
# Get a list of groups.
groups = []
for item in os.listdir(config["dataFolder"] + os.sep + "Groups"):
  if item.startswith("KS-SEC-PUPILS-"):
    groups.append(item[14:])
    
print(groups)

# Read the Courses list. Courses CSV headings:
# id,name,courseState,descriptionHeading,description,section,room,enrollmentCode,guardiansEnabled,alternateLink,ownerId,creationTime,updateTime,calendarId,courseGroupEmail,teacherGroupEmail,teacherFolder.id,teacherFolder.title,teacherFolder.alternateLink,courseMaterialSets,courseMaterialSets.0.materials.0.driveFile.alternateLink,courseMaterialSets.0.materials.0.driveFile.id,courseMaterialSets.0.materials.0.driveFile.title,courseMaterialSets.0.title
courses = pandas.read_csv(config["dataFolder"] + os.sep + "courses.csv", header=0)

unHandledCourses = []
for courseIndex, course in courses.iterrows():
  if course["courseState"] == "ACTIVE":
    formFound = False
    for group in group:
      if group in normaliseYearNames(course["name"]):
        groupFound = True
        print("Assign " + group + " to " + course["name"])
        # Read the existing basic pupils data.
        #pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
    if groupFound == False:
      unHandledCourses.append(course["name"])

print("Unhandled courses:")
print(unHandledCourses)
#installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "KS-SEC-STAFF.csv", outputString)
