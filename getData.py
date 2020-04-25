#!/usr/bin/python
import os
import io
import ssl
import json
import pandas
import dataLib
import urllib.request

requiredConfigParameters = ["iSAMSAPIKey", "iSAMSAPIDomain"]

# Load the configuration file.
config = json.loads(dataLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

# Go and get the data from the iSAMS API.
print("Getting data from iSAMS.")
response = urllib.request.urlopen("https://" + config["iSAMSAPIDomain"] + "/api/batch/1.0/xml.ashx?apiKey=" + config["iSAMSAPIKey"], context=ssl._create_unverified_context())
dataLib.writeFile("iSAMSData.xml", str(response.read())[2:-1])

print("Getting users list from GSuite.")
users = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print users allfields")))
users.to_csv(config["dataFolder"] + os.sep + "users.csv", index=False)

# Get a list of all courses, output in CSV format directly from GAM.
print("Getting course list from Google Classroom.")
os.system("gam print courses > \"" + config["dataFolder"] + os.sep + "courses.csv\"")

print("Getting groups list from GSuite.")
os.system("gam print groups name description admincreated id aliases members owners managers settings > \"" + config["dataFolder"] + os.sep + "groups.csv\"")

print("Getting guardians list from GSuite.")
guardians = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print guardians")))
for guardiansIndex, guardiansValue in guardians.iterrows():
	for usersIndex, usersValue in users.iterrows():
		if usersValue["id"] == guardiansValue["studentId"]:
			guardians.at[guardiansIndex, "studentEmail"] = usersValue["primaryEmail"]
guardians.to_csv(config["dataFolder"] + os.sep + "guardians.csv", index=False)

guardianInvitations = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print guardians invitations")))
for guardianInvitationsIndex, guardianInvitationsValue in guardianInvitations.iterrows():
	for usersIndex, usersValue in users.iterrows():
		if usersValue["id"] == guardianInvitationsValue["studentId"]:
			guardianInvitations.at[guardianInvitationsIndex, "studentEmail"] = usersValue["primaryEmail"]
guardianInvitations.to_csv(config["dataFolder"] + os.sep + "guardianInvitations.csv", index=False)
