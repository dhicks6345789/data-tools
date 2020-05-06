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

activity = pandas.read_csv(config["dataFolder"] + os.sep + "Reports" + os.sep + "userActivity.csv", header=0)
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

for activityIndex, activityValues in activity.iterrows():
	username = activityValues["email"].split("@")[0]
	for pupilsIndex, pupilsValues in pupils.iterrows():
		if pupilsValues["OldUsername"] == username and username.endswith("17") and activityValues["accounts:last_login_time"] == "Never":
			print("gam delete user " + username)
			print("gam make alias for " + pupilsValues["Username"] + " as " + username)
