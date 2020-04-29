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
cachePupilsSyncRoot = cacheRoot + os.sep + "pupilsSync"
os.makedirs(cachePupilsSyncRoot, exist_ok=True)
cachePupilsAddRoot = cacheRoot + os.sep + "pupilsAdd"
os.makedirs(cachePupilsAddRoot, exist_ok=True)
cacheTeachersSyncRoot = cacheRoot + os.sep + "teachersSync"
os.makedirs(cacheTeachersSyncRoot, exist_ok=True)
cacheTeachersAddRoot = cacheRoot + os.sep + "teachersAdd"
os.makedirs(cacheTeachersAddRoot, exist_ok=True)

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
pupilUsernames = pupils["OldUsername"].tolist()

if len(sys.argv) > 1:
	if sys.argv[1] == "-flushCache":
		os.system("erase \"" + cachePupilsSyncRoot + os.sep + "*.csv\"")
		os.system("erase \"" + cacheTeachersSyncRoot + os.sep + "*.csv\"")
		os.system("erase \"" + cachePupilsAddRoot + os.sep + "*.csv\"")
		os.system("erase \"" + cacheTeachersAddRoot + os.sep + "*.csv\"")

# Load the "classroomToSync" spreadsheet. Should consist of four columns:
# Classroom: Classroom name.
# Sync Or Add?: Whether to sync the list of users / groups given or whether to add to any existing members.
# Pupils: Users or Groups to set as pupils.
# Teachers: Users or Groups to set as teachers.
(options, classrooms) = dataLib.readOptionsFile(classroomsRoot + os.sep + "classroomsToSync.xlsx", ["Classroom","Sync Or Add?","Pupils","Teachers"])
for classroomsIndex, classroomsValue in classrooms.iterrows():
	classroomName = dataLib.noNan(classroomsValue["Classroom"])
	if not classroomName == "":
		syncValue = dataLib.noNan(classroomsValue["Sync Or Add?"])
		pupilsList = dataLib.noNan(classroomsValue["Pupils"])
		teachersList = dataLib.noNan(classroomsValue["Teachers"])
		pupilsCSV = ""
		teachersCSV = ""
		for pupilsItem in pupilsList.split(","):
			pupilsItem = pupilsItem.strip()
			groupPath = groupsRoot + os.sep + pupilsItem + ".csv"
			if os.path.exists(csvPath):
				pupilsCSV = pupilsCSV + dataLib.readFile(csvPath)
			elif pupilsItem in pupilUsernames:
				pupilsCSV = pupilsCSV + "\n" + pupilsItem
			else:
				print("Unknown group or user: " + pupilsItem)
		if syncValue == "sync" and not pupilsCSV == "":
			pupilsSyncCacheFile = cachePupilsSyncRoot + os.sep + classroomName + ".csv"
			if dataLib.rewriteCachedData(pupilsSyncCacheFile, pupils):
				classroomID = ""
				for classroomIndex, classroomValue in classrooms.iterrows():
					if classroomValue["courseState"] == "ACTIVE" and classroomValue["name"] == classroomName:
						print("Syncing: " + classroomValue["name"])
						classroomID = dataLib.noNan(str(classroomValue["id"]))
						print("gam course " + classroomID + " sync students file " + pupilsSyncCacheFile)
