#!/usr/bin/python
import os
import re
import io
import sys
import pandas
import dataLib

# A function to remove "nan" strings from data - /really/ shouldn't be needed...
def noNan(theString):
	if str(theString) == "nan" or str(theString) == "0":
		return ""
	return str(theString.strip())

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

groupsRoot = config["dataFolder"] + os.sep + "Groups"

# Get a current list of Google Classrooms.
classrooms =  pandas.read_csv(io.StringIO(dataLib.runCommand("gam print courses")))

# Load the "classroomsToSync" spreadsheet. Should simply consist of two columns, one listing Classrooms (by title), the other the groups(s)
# to sync with that Classroom.
classroomsDataframe = pandas.read_excel(config["dataFolder"] + os.sep + "classroomsToSync.xlsx", header=None)
for classroomIndex, classroomValue in classroomsDataframe.iterrows():
	if not classroomIndex == 0:
		classroomName = noNan(classroomsDataframe.at[classroomIndex, 0])
		if not classroomName == "":
			pupilsGroups = classroomsDataframe.at[classroomIndex, 1]
			teachersGroups = classroomsDataframe.at[classroomIndex, 2]
			pupils = ""
			for pupilsGroup in pupilsGroups.split(","):
				csvPath = groupsRoot + os.sep + pupilsGroup.strip() + ".csv"
				if os.path.exists(csvPath):
					pupils = pupils + dataLib.readFile(csvPath)
				else:
					print("Unknown group: " + pupilsGroup.strip())
			if not pupils == "":
				dataLib.writeFile("pupilsData.csv", pupils)
				classroomID = ""
				for classroomIndex, classroomValue in classrooms.iterrows():
					if classroomValue["name"] == classroomName:
						classroomID = noNan(str(classroomValue["id"]))
						print("gam course " + classroomID + " sync students file pupilsData.csv")
				os.remove("pupilsData.csv")
