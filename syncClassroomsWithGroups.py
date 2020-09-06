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

def syncOrAdd(teacherOrStudent, syncValue, classroomName, cacheFile, CSVData):
	if dataLib.rewriteCachedData(cacheFile, CSVData):
		for coursesIndex, coursesValue in courses.iterrows():
			if classroomName == coursesValue["name"]:
				print("Now " + syncValue + "ing: " + classroomName)
				if syncValue == "sync":
					gamCommand = "gam course " + dataLib.noNan(coursesValue["id"]) + " sync " + teacherOrStudent + "s file \"" + cacheFile + "\""	
					if "-test" in sys.argv:
						print(gamCommand)
					else:
						os.system(gamCommand)
				else:
					for user in CSVData.split("\n"):
						user = user.strip()
						if not user == "":
							if user.startswith("ks") and user[-2:] in ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]:
								print user
							gamCommand = "gam course " + dataLib.noNan(coursesValue["id"]) + " add " + teacherOrStudent + " " + user
							if "-test" in sys.argv:
								print(gamCommand)
							else:
								os.system(gamCommand)

# Read the users data.
users = pandas.read_csv(config["dataFolder"] + os.sep + "users.csv", header=0)
usernames = users["primaryEmail"].tolist()

# Read the existing courses (Classrooms) data.
courses = pandas.read_csv(config["dataFolder"] + os.sep + "courses.csv", header=0)

if "-flushCache" in sys.argv:
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
		cachePupilsRoot = cachePupilsSyncRoot
		cacheTeachersRoot = cacheTeachersSyncRoot
		if syncValue == "add":
			cachePupilsRoot = cachePupilsAddRoot
			cacheTeachersRoot = cacheTeachersAddRoot
		
		pupilsCSV = ""
		pupilsList = dataLib.noNan(classroomsValue["Pupils"])
		for pupilsItem in pupilsList.split(","):
			pupilsItem = pupilsItem.strip()
			if not pupilsItem == "":
				groupPath = groupsRoot + os.sep + pupilsItem + ".csv"
				if os.path.exists(groupPath):
					pupilsCSV = pupilsCSV + dataLib.readFile(groupPath)
				elif pupilsItem + "@knightsbridgeschool.com" in usernames:
					pupilsCSV = pupilsCSV + "\n" + pupilsItem
				else:
					print("Unknown group or user in pupils list: " + pupilsItem)

		teachersCSV = ""
		teachersList = dataLib.noNan(classroomsValue["Teachers"])
		for teachersItem in teachersList.split(","):
			teachersItem = teachersItem.strip()
			if not teachersItem == "":
				groupPath = groupsRoot + os.sep + teachersItem + ".csv"
				if os.path.exists(groupPath):
					teachersCSV = teachersCSV + dataLib.readFile(groupPath)
				elif teachersItem + "@knightsbridgeschool.com" in usernames:
					teachersCSV = teachersCSV + "\n" + teachersItem
				else:
					print("Unknown group or user in teachers list: " + teachersItem)
		
		if not pupilsCSV == "" and (syncValue == "sync" or syncValue == "add"):
			syncOrAdd("student", syncValue, classroomName, cachePupilsRoot + os.sep + classroomName + ".csv", pupilsCSV)
			
		if not teachersCSV == "" and (syncValue == "sync" or syncValue == "add"):
			syncOrAdd("teacher", syncValue, classroomName, cacheTeachersRoot + os.sep + classroomName + ".csv", teachersCSV)
