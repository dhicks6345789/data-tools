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

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
oldPupilUsernames = pupils["OldUsername"].tolist()
newPupilUsernames = pupils["Username"].tolist()

activity = pandas.read_csv(config["dataFolder"] + os.sep + "Reports" + os.sep + "userActivity.csv", header=0)

for activityIndex, activityValues in activity.iterrows():
	username = activityValues["email"].split("@")[0]
	if username in newPupilUsernames and activityValues["accounts:last_login_time"] == "Never":
		print(username)
