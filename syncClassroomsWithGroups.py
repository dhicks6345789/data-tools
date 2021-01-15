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

def getCommandOutput(theCommand):
	commandHandle = os.popen(theCommand)
	result = commandHandle.read()
	commandHandle.close()
	return(result)

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
							if user.startswith("ks") and user.split("@")[0][-2:] in ["11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23"]:
								for pupilsIndex, pupilsValue in pupils.iterrows():
									if user == pupilsValue["OldUsername"] + "@knightsbridgeschool.com":
										gamCommand = "gam course " + dataLib.noNan(coursesValue["id"]) + " add " + teacherOrStudent + " " + pupilsValue["Username"]
							else:
								gamCommand = "gam course " + dataLib.noNan(coursesValue["id"]) + " add " + teacherOrStudent + " " + user
							if "-test" in sys.argv:
								print(gamCommand)
							else:
								os.system(gamCommand)

def cacheGroups(cacheFile, groups):
	groupContents = ""
	for group in groups.split(","):
		infile = open(groupsRoot + os.sep + group + ".csv")
		groupContents = groupContents + infile.read()
		infile.close()
	outfile = open(cacheRoot + os.sep + cacheFile, "w")
	outfile.write(groupContents)
	outfile.close()

# Read the users data.
users = pandas.read_csv(config["dataFolder"] + os.sep + "users.csv", header=0)
usernames = users["primaryEmail"].tolist()

# This bit should just be temporary.
#pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Get a list of all courses, output in CSV format directly from GAM.
print("Getting course list from Google Classroom.")
classrooms = pandas.read_csv(io.StringIO(getCommandOutput("gam print courses states ACTIVE")))

# Get the list of Pupil Groups to match with strings in Classroom names.
pupilGroups = {}
for pupilGroupsIndex, pupilGroupsValue in pandas.read_excel(classroomsRoot + os.sep + "pupilGroups.xlsx", header=None).iterrows():
	pupilGroups[pupilGroupsValue[0]] = pupilGroupsValue[1]

# Get the list of Teacher Groups to match with strings in Classroom names.
teacherGroups = {}
for teacherGroupsIndex, teacherGroupsValue in pandas.read_excel(classroomsRoot + os.sep + "teacherGroups.xlsx", header=None).iterrows():
	teacherGroups[teacherGroupsValue[0]] = teacherGroupsValue[1]

# Read the existing courses (Classrooms) data.
#courses = pandas.read_csv(config["dataFolder"] + os.sep + "courses.csv", header=0)

if "-flushCache" in sys.argv:
	os.system("erase \"" + cachePupilsSyncRoot + os.sep + "*.csv\"")
	os.system("erase \"" + cacheTeachersSyncRoot + os.sep + "*.csv\"")
	os.system("erase \"" + cachePupilsAddRoot + os.sep + "*.csv\"")
	os.system("erase \"" + cacheTeachersAddRoot + os.sep + "*.csv\"")

# "ID", "Classroom","Sync Or Add?","Pupils","Teachers"
classroomsToSync = pandas.read_excel(classroomsRoot + os.sep + "classroomsToSync.xlsx", header=0)
classroomsToSyncIDs = classroomsToSync["ID"].tolist()
classroomsToAppend = []
for classroomsIndex, classroomsValue in classrooms.iterrows():
	if not classroomsValue["id"] in classroomsToSyncIDs:
		pupilsString = ""
		for pupilMatch in pupilGroups.keys():
			if pupilsString == "" and pupilMatch.lower() in classroomsValue["name"].lower():
				pupilsString = pupilGroups[pupilMatch]
				
		teachersString = ""
		for teacherMatch in teacherGroups.keys():
			if teachersString == "" and teacherMatch.lower() in classroomsValue["name"].lower():
				teachersString = teacherGroups[teacherMatch]
				
		classroomsToAppend.append({"ID":classroomsValue["id"], "Classroom":classroomsValue["name"], "Sync Or Add?":"", "Pupils":pupilsString, "Teachers":teachersString})
classroomsToSync = classroomsToSync.append(pandas.DataFrame(classroomsToAppend))
classroomsToSync.to_excel(classroomsRoot + os.sep + "classroomsToSync.xlsx", index=False)

# "ID", "Classroom","Sync Or Add?","Pupils","Teachers"
for classroomsToSyncIndex, classroomsToSyncValue in classroomsToSync.iterrows():
	classroomID = dataLib.noNan(classroomsToSyncValue["ID"])
	classroomName = dataLib.noNan(classroomsToSyncValue["Classroom"])
	classroomSyncOrAdd = dataLib.noNan(classroomsToSyncValue["Sync Or Add?"])
	classroomPupils = dataLib.noNan(classroomsToSyncValue["Pupils"])
	classroomTeachers = dataLib.noNan(classroomsToSyncValue["Teachers"])
	if classroomSyncOrAdd == "sync" and not classroomPupils == "":
		cacheGroups("pupilsSync" + classroomID, classroomPupils)
