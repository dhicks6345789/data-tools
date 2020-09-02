import os
import io
import sys
import json
import pandas
import dataLib

validYears = ["12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22"]

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
reportsRoot = config["dataFolder"] + os.sep + "Reports"

activity = pandas.read_csv(config["dataFolder"] + os.sep + "Reports" + os.sep + "userActivity.csv", header=0)
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

allUsersHandle = os.popen("gam print users")
allUsersData = allUsersHandle.read()
allUsersHandle.close()
for allUsersLine in allUsersData.split("\n"):
	if allUsersLine.startswith("ks") and allUsersLine.split("@")[0][-2:] in validYears:
		print(allUsersLine)

for pupilsIndex, pupilsValues in pupils.iterrows():
	print(pupilsValues["OldUsername"] + " to " + pupilsValues["Username"])

#for activityIndex, activityValues in activity.iterrows():
#	username = activityValues["email"].split("@")[0]
#	for pupilsIndex, pupilsValues in pupils.iterrows():
#		if pupilsValues["Username"] == username and username.endswith("17") and activityValues["accounts:last_login_time"] == "Never":
#			print("gam delete user " + username)
#			#print("gam create alias " + username + " user " + pupilsValues["OldUsername"])
