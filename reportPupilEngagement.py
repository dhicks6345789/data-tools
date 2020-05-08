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

report = pandas.DataFrame(columns=["Name","Username","Yeargroup","AccountsLastLoginTime","ClassroomLastInteractionTime"])

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
					indexToUse = reportIndex
					usernameList = report["Username"].tolist()
					if altUsername in usernameList:
						altUsernameIndex = usernameList.index(altUsername)
						if report.at[altUsernameIndex, "AccountsLastLoginTime"] == "Never":
							indexToUse = altUsernameIndex
					else:
						reportIndex = reportIndex + 1
					report.at[indexToUse, "Name"] = pupilsValues["GivenName"] + " " + pupilsValues["FamilyName"]
					report.at[indexToUse, "Username"] = username
					report.at[indexToUse, "Yeargroup"] = yearGroup
					report.at[indexToUse, "AccountsLastLoginTime"] = activityValues["accounts:last_login_time"]
					report.at[indexToUse, "ClassroomLastInteractionTime"] = activityValues["classroom:last_interaction_time"]

# Write out the CSV report.
report.to_csv(outputRoot + os.sep + "report.csv", index=False)

#for yearGroup in yearGroups.keys():
#	for reportIndex, reportValues in report.iterrows():
#		if reportValues["Yeargroup"] == yearGroup:
#			print(reportValues)
