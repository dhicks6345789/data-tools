#!/usr/bin/python
import os
import re
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
	os.system("gam create guardianinvite " + str(theGuardian) + " " + theUsername + "@knightsbridgeschool.com")

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Read the existing Guardians list, i.e. accounts that have confirmed Guardians. Fields:
# studentEmail,studentId,invitedEmailAddress,guardianId,guardianProfile.emailAddress,guardianProfile.id,guardianProfile.name.familyName,guardianProfile.name.fullName,guardianProfile.name.givenName,guardianProfile.photoUrl
guardians = pandas.read_csv(config["dataFolder"] + os.sep + "guardians.csv", header=0)

if len(sys.argv) >= 3:
	if len(sys.argv) == 3 and sys.argv[1] == "-user":
		username = sys.argv[2]
		for pupilIndex, pupilEntry in pupils.iterrows():
			if pupilEntry["OldUsername"] == username:
				inviteGuardian(username, pupilEntry["MainContact"])
	elif len(sys.argv) == 3 and sys.argv[1] == "-group":
		groupname = sys.argv[2]
		for pupilsIndex, pupilsValue in pupils.iterrows():
			if groupname in pupilsValue["Form"]:
				for contact in noNan(pupilsValue["Contacts"]).split(" "):
					contact = contact.strip()
					if not contact == "":
						sendInviate = True
						for guardiansIndex, guardiansValue in guardians.iterrows():
							if pupilsValue["OldUsername"] == guardiansValue["studentEmail"].split("@")[0]:
								print("Already has Guardian: " + pupilsValue["OldUsername"])
								sendInviate = False
					if sendInviate:
						inviteGuardian(pupilsValue["OldUsername"], contact)
