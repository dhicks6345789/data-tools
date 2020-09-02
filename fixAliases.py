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

allUsersHandle = os.popen("gam print users")
allUsersData = allUsersHandle.read()
allUsersHandle.close()
for allUsersLine in allUserData.split("\n"):
	print(allUsersLine)

#for pupilsIndex, pupilsValues in pupils.iterrows():
#	print(pupilsValues["OldUsername"] + " to " + pupilsValues["Username"])

#for activityIndex, activityValues in activity.iterrows():
#	username = activityValues["email"].split("@")[0]
#	for pupilsIndex, pupilsValues in pupils.iterrows():
#		if pupilsValues["Username"] == username and username.endswith("17") and activityValues["accounts:last_login_time"] == "Never":
#			print("gam delete user " + username)
#			#print("gam create alias " + username + " user " + pupilsValues["OldUsername"])
