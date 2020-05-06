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

#resultIndex = 0
#count = 0
yearGroups = {}
for pupilsIndex, pupilsValues in pupils.iterrows():
	yearGroups[pupilsValues["YearGroup"]] = 1
for yearGroup in yearGroups.keys():
	for pupilsIndex, pupilsValues in pupils.iterrows():
		if pupilsValues["YearGroup"] == yearGroup:
			for activityIndex, activityValues in activity.iterrows():
				if activityValues["email"] == pupilsValues["OldUsername"] + "@knightsbridgeschool.com":
					print(activityValues["email"])

#parentsAsPupils.to_csv(outputRoot + os.sep + "report.csv", index=False)
