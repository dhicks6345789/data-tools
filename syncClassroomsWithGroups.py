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

# Load the "classroomsToSync" spreadsheet. Should simply consist of two columns, one listing Classrooms (by title), the other the groups(s)
# to sync with that Classroom.
classroomsDataframe = pandas.read_excel(config["dataFolder"] + os.sep + "classroomsToSync.xlsx", header=None)
for classroomIndex, classroomValue in classroomDataframe.iterrows():
	if not classroomIndex == 0:
		classroomName = noNan(optionsDataframe.at[classroomIndex, 0])
		if not classroomName == "":
			classroomGroup = optionsDataframe.at[classroomIndex, 1]
			if not classroomGroup == "":
				print(classroomName)
				print(classroomGroup)
