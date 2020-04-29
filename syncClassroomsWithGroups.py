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

if len(sys.argv) > 1:
	if sys.argv[1] == "-flushCache":
		os.system("erase \"" + cachePupilsSyncRoot + os.sep + "*.csv\"")
		os.system("erase \"" + cacheTeachersSyncRoot + os.sep + "*.csv\"")
		os.system("erase \"" + cachePupilsAddRoot + os.sep + "*.csv\"")
		os.system("erase \"" + cacheTeachersAddRoot + os.sep + "*.csv\"")

# Get a current list of Google Classrooms.
(options, classrooms) = dataLib.readOptionsFile(classroomsRoot + os.sep + "classrooms.xlsx", ["Classroom","Sync Or Add?","Pupils","Teachers"])

classroomsList = classrooms["Classroom"].tolist()
classroomCount = len(classroomsList)
for classroomIndex, classroomValue in pandas.read_csv(io.StringIO(dataLib.runCommand("gam print courses"))).iterrows():
	if classroomValue["courseState"] == "ACTIVE" and not classroomValue["name"] in classroomsList:
		classrooms.at[classroomCount, "Classroom"] = classroomValue["name"]
		classroomCount = classroomCount + 1

dataLib.writeDataframeFile(classroomsRoot + os.sep + "classrooms.xlsx", classrooms)

sys.exit(0)

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
			pupilsSyncCacheFile = cachePupilsSyncRoot + os.sep + classroomName + ".csv"
			if dataLib.rewriteCachedData(pupilsSyncCacheFile, pupils):
				classroomID = ""
				for classroomIndex, classroomValue in classrooms.iterrows():
					if classroomValue["courseState"] == "ACTIVE" and classroomValue["name"] == classroomName:
						print("Syncing: " + classroomValue["name"])
						classroomID = dataLib.noNan(str(classroomValue["id"]))
						print("gam course " + classroomID + " sync students file " + pupilsSyncCacheFile)
			teachersSyncCacheFile = cacheTeachersSyncRoot + os.sep + classroomName + ".csv"
			if dataLib.rewriteCachedData(teachersSyncCacheFile, teachers.replace(",","\n").strip()):
				print("gam course " + classroomID + " sync teachers file " + teachersSyncCacheFile)
