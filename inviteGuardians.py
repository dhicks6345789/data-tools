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

# Set the root folder.
guardiansRoot = config["dataFolder"] + os.sep + "Guardians"
os.makedirs(guardiansRoot, exist_ok=True)

# Read the users data. Used for cross-referencing Google IDs with usernames.
users = pandas.read_csv(config["dataFolder"] + os.sep + "users.csv", header=0)	

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# If the user has specified the "-getData" parameter, go and get a Guardians report from GSuite.
# We get the basic report using GAM, then match up GSuite user IDs with usernames.
if len(sys.argv) == 2 and sys.argv[1] == "-getData":
	print("Getting guardians list from GSuite.")
	guardians = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print guardians invitations")))
	for guardiansIndex, guardiansValue in guardians.iterrows():
		for usersIndex, usersValue in users.iterrows():
			if usersValue["id"] == guardiansValue["studentId"]:
				guardians.at[guardiansIndex, "studentEmail"] = usersValue["primaryEmail"]
	guardians.to_csv(guardiansRoot + os.sep + "guardians.csv", index=False)

# Read the existing Guardians list (might have just been updated in the section above). Fields:
# studentEmail,studentId,invitedEmailAddress,invitationId,creationTime,state
guardians = pandas.read_csv(guardiansRoot + os.sep + "guardians.csv", header=0)

# If a pupil / parent combination without a Guardian request exists, create a new Guardian request.
maxNumContacts = 0
completedInvites = {}
invitedEmailAddresses = guardians["invitedEmailAddress"].tolist()
for pupilsIndex, pupilsValue in pupils.iterrows():
	completedInvites[pupilsValue["OldUsername"]] = False
	maxNumContacts = max(maxNumContacts, len(noNan(pupilsValue["Contacts"]).split(" ")))
	for contact in noNan(pupilsValue["Contacts"]).split(" "):
		contact = contact.strip()
		if not contact == "" and not contact in invitedEmailAddresses:
			print("Sending invite for " + pupilsValue["OldUsername"] + " to " + contact)
			#os.system("gam create guardianinvite " + str(contact) + " " + pupilsValue["OldUsername"] + "@knightsbridgeschool.com")

for guardiansIndex, guardiansValue in guardians.iterrows():
	for pupilsIndex, pupilsValue in pupils.iterrows():
		if guardiansValue["studentEmail"] == pupilsValue["OldUsername"] + "@knightsbridgeschool.com" and guardiansValue["state"] == "COMPLETE":
			completedInvites[pupilsValue["OldUsername"]] = True

reportIndex = 1
guardiansColumns = ["Name", "Username", "Yeargroup", "Form"]
for pl in range(1, maxNumContacts):
	guardiansColumns.append("Contacts" + str(pl))
	guardiansColumns.append("Sent" + str(pl))
pupilsNoGuardians = pandas.DataFrame(columns=guardiansColumns)
for pupilUsername in completedInvites.keys():
	if not completedInvites[pupilUsername]:
		for pupilsIndex, pupilsValue in pupils.iterrows():
			if pupilsValue["OldUsername"] == pupilUsername:
				pupilsNoGuardians.at[reportIndex, "Name"] = pupilsValue["GivenName"] + " " + pupilsValue["FamilyName"]
				pupilsNoGuardians.at[reportIndex, "Username"] = pupilsValue["OldUsername"]
				pupilsNoGuardians.at[reportIndex, "Yeargroup"] = pupilsValue["YearGroup"]
				pupilsNoGuardians.at[reportIndex, "Form"] = pupilsValue["Form"]
				pupilsNoGuardians.at[reportIndex, "Contacts1"] = pupilsValue["Contacts"]
				reportIndex = reportIndex + 1
pupilsNoGuardians.to_excel(guardiansRoot + os.sep + "pupilsWithNoConfirmedGuardians.xlsx", index=False)
