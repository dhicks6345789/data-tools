#!/usr/bin/python
import os
import re
import io
import sys
import csv
import json
import pandas
import random
import dataLib

# A function to remove "nan" strings from data - /really/ shouldn't be needed...
def noNan(theString):
	if str(theString) == "nan" or str(theString) == "0":
		return ""
	return str(theString)

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

def inviteGuardian(theUsername, theGuardian):
	print("Sending invite for " + theUsername)
	print("gam create guardianinvite " + str(theGuardian) + " " + theUsername + "@knightsbridgeschool.com")

# Read the users data. Used for cross-referencing Google IDs with usernames.
users = pandas.read_csv(config["dataFolder"] + os.sep + "users.csv", header=0)	

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

if len(sys.argv) == 2 and sys.argv[1] == "-getData":
	print("Getting guardians list from GSuite.")
	guardians = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print guardians invitations")))
	for guardiansIndex, guardiansValue in guardians.iterrows():
		for usersIndex, usersValue in users.iterrows():
			if usersValue["id"] == guardiansValue["studentId"]:
				guardians.at[guardiansIndex, "studentEmail"] = usersValue["primaryEmail"]
	guardians.to_csv(config["dataFolder"] + os.sep + "guardians.csv", index=False)

# Read the existing Guardians list. Fields:
# studentEmail,studentId,invitedEmailAddress,invitationId,creationTime,state
guardians = pandas.read_csv(config["dataFolder"] + os.sep + "guardians.csv", header=0)

invitedEmailAddresses = guardians["invitedEmailAddress"].tolist()
for pupilsIndex, pupilsValue in pupils.iterrows():
	for contact in noNan(pupilsValue["Contacts"]).split(" "):
		if not contact in invitedEmailAddresses:
			inviteGuardian(pupilsValue["OldUsername"], contact)
