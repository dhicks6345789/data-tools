#!/usr/bin/python
import os
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

def getCommandOutput(theCommand):
	commandHandle = os.popen(theCommand)
	result = commandHandle.read()
	commandHandle.close()
	return(result)

def cacheGroups(cacheFile, groups):
	groupContents = ""
	for group in groups.split(","):
		infile = open(groupsRoot + os.sep + group + ".csv")
		groupContents = groupContents + infile.read()
		infile.close()
	outfile = open(cacheFile, "w")
	outfile.write(groupContents)
	outfile.close()

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
	
	gamCommand = ""
	cacheFile = ""
	if classroomSyncOrAdd == "sync" and not classroomPupils == "":
		cacheFile = cacheRoot + os.sep + "pupilsSync" + classroomID + ".csv"
		cacheGroups(cacheFile, classroomPupils)
		gamCommand = "gam course " + classroomID + " sync pupils file \"" + cacheFile + "\""
	if not gamCommand == "":
		print(gamCommand)
		#if "-test" in sys.argv:
		#print(gamCommand)
		#else:
		#os.system(gamCommand)
