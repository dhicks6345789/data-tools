#!/usr/bin/python
import os
import io
import sys
import json
import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
reportsRoot = config["dataFolder"] + os.sep + "Reports"
outputRoot = reportsRoot + os.sep + "Parents Joined To Classrooms As Pupils"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Parents:
# Output in CSV format:
parentsAsPupils = pandas.DataFrame(columns=["First Name","Last Name","Email","Classroom Name","Classroom ID","Classroom Teachers"])

parents = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
courses = pandas.read_csv(config["dataFolder"] + os.sep + "courses.csv", header=0)

resultIndex = 0
count = 0
for coursesIndex, coursesValues in courses.iterrows():
	count = count + 1
	if count < 1000:
		# CSV Format from GAM report:
		# courseId,courseName,userRole,userId,profile.emailAddress,profile.id,profile.name.familyName,profile.name.fullName,profile.name.givenName,profile.permissions,profile.permissions.0.permission,profile.photoUrl,profile.verifiedTeacher
		members = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print course-participants course " + str(coursesValues["id"]) + " show all")))
		for membersIndex, membersValues in members.iterrows():
			if not membersValues["profile.emailAddress"].endswith("@knightsbridgeschool.com"):
				parentsAsPupils.at[resultIndex, "Email"] = membersValues["profile.emailAddress"]
				parentsAsPupils.at[resultIndex, "Classroom Name"] = str(coursesValues["name"])
				parentsAsPupils.at[resultIndex, "Classroom ID"] = str(coursesValues["id"])
				resultIndex = resultIndex + 1
	
parentsAsPupils.to_csv(outputRoot + os.sep + "report.csv", index=False)
