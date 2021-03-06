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
	username = allUsersLine.split("@")[0]
	if allUsersLine.startswith("ks") and username[-2:] in validYears:
		for pupilsIndex, pupilsValues in pupils.iterrows():
			if username == pupilsValues["OldUsername"]:
				os.system("gam create datatransfer " + pupilsValues["OldUsername"] + "@knightsbridgeschool.com drive " + pupilsValues["Username"] + "@knightsbridgeschool.com all")

#for activityIndex, activityValues in activity.iterrows():
#	username = activityValues["email"].split("@")[0]
#	for pupilsIndex, pupilsValues in pupils.iterrows():
#		if pupilsValues["Username"] == username and username.endswith("17") and activityValues["accounts:last_login_time"] == "Never":
#			print("gam delete user " + username)
#			#print("gam create alias " + username + " user " + pupilsValues["OldUsername"])
