#!/usr/bin/python
import os
import re
import io
import sys
import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

groupsRoot = config["dataFolder"] + os.sep + "Groups"
classroomsRoot = config["dataFolder"] + os.sep + "Classrooms"
os.makedirs(classroomsRoot, exist_ok=True)
cacheRoot = classroomsRoot + os.sep + "CSVs"
os.makedirs(cacheRoot, exist_ok=True)

# Get a current list of Google Classrooms.
classrooms =  pandas.read_csv(io.StringIO(dataLib.runCommand("gam print courses")))

# Load the "classroomsToSync" spreadsheet. Should simply consist of two columns, one listing Classrooms (by title), the other the groups(s)
# to sync with that Classroom.
classroomsDataframe = pandas.read_excel(classroomsRoot + os.sep + "classroomsToSync.xlsx", header=None)
for classroomIndex, classroomValue in classroomsDataframe.iterrows():
	if not classroomIndex == 0:
		classroomName = dataLib.noNan(classroomsDataframe.at[classroomIndex, 0])
		if not classroomName == "":
			pupilsGroups = dataLib.noNan(classroomsDataframe.at[classroomIndex, 1])
			teachers = dataLib.noNan(classroomsDataframe.at[classroomIndex, 2])
			pupils = ""
			for pupilsGroup in pupilsGroups.split(","):
				csvPath = groupsRoot + os.sep + pupilsGroup.strip() + ".csv"
				if os.path.exists(csvPath):
					pupils = pupils + dataLib.readFile(csvPath)
				else:
					print("Unknown group: " + pupilsGroup.strip())
			#if not pupils == "":
			if dataLib.rewriteCachedData(cacheRoot + os.sep + classroomName + ".csv", pupils):
				dataLib.writeFile("pupilsData.csv", pupils)
				classroomID = ""
				for classroomIndex, classroomValue in classrooms.iterrows():
					if classroomValue["courseState"] == "ACTIVE" and classroomValue["name"] == classroomName:
						print("Syncing: " + classroomValue["name"])
						classroomID = dataLib.noNan(str(classroomValue["id"]))
						print("gam course " + classroomID + " sync students file pupilsData.csv")
				os.remove("pupilsData.csv")
			if not teachers == "":
				dataLib.writeFile("teachersData.csv", teachers.replace(",","\n").strip())
				os.system("gam course " + classroomID + " sync teachers file teachersData.csv")
				os.remove("teachersData.csv")
