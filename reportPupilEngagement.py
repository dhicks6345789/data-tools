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
outputRoot = reportsRoot + os.sep + "Pupil Engagement"
os.makedirs(outputRoot, exist_ok=True)

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
activity = pandas.read_csv(config["dataFolder"] + os.sep + "Reports" + os.sep + "userActivity.csv", header=0)

report = pandas.DataFrame(columns=["Name","Username","Yeargroup","ClassroomLastInteractionTime"])

yearGroups = {}
for pupilsIndex, pupilsValues in pupils.iterrows():
	yearGroups[pupilsValues["YearGroup"]] = 1
reportIndex = 0
for yearGroup in yearGroups.keys():
	for pupilsIndex, pupilsValues in pupils.iterrows():
		if pupilsValues["YearGroup"] == yearGroup:
			for activityIndex, activityValues in activity.iterrows():
				username = ""
				if activityValues["email"] == pupilsValues["Username"] + "@knightsbridgeschool.com":
					username = pupilsValues["Username"]
					altUsername = pupilsValues["OldUsername"]
				elif activityValues["email"] == pupilsValues["OldUsername"] + "@knightsbridgeschool.com":
					username = pupilsValues["OldUsername"]
					altUsername = pupilsValues["Username"]
				if not username == "":
					usernameList = report["Username"].tolist()
					if altUsername in usernameList:
						altUsernameIndex = usernameList.index(altUsername)
						if report.at[altUsernameIndex, "ClassroomLastInteractionTime"] == "Never":
							if not activityValues["classroom:last_interaction_time"] == "Never":
								report.at[altUsernameIndex, "Name"] = pupilsValues["GivenName"] + " " + pupilsValues["FamilyName"]
								report.at[altUsernameIndex, "Username"] = altUsername
								report.at[altUsernameIndex, "Yeargroup"] = yearGroup
								report.at[altUsernameIndex, "ClassroomLastInteractionTime"] = activityValues["classroom:last_interaction_time"]
					else:
						report.at[reportIndex, "Name"] = pupilsValues["GivenName"] + " " + pupilsValues["FamilyName"]
						report.at[reportIndex, "Username"] = username
						report.at[reportIndex, "Yeargroup"] = yearGroup
						report.at[reportIndex, "ClassroomLastInteractionTime"] = activityValues["classroom:last_interaction_time"]
						reportIndex = reportIndex + 1

report.to_csv(outputRoot + os.sep + "report.csv", index=False)
