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
	print("gam create guardianinvite " + str(theGuardian) + " " + theUsername + "@knightsbridgeschool.com")
		
# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

if len(sys.argv) >= 3:
	if len(sys.argv) == 3 and sys.argv[1] == "-user":
		username = sys.argv[2]
		for pupilIndex, pupilEntry in pupils.iterrows():
			if pupilEntry["OldUsername"] == username:
				inviteGuardian(username, pupilEntry["MainContact"])
	elif len(sys.argv) == 3 and sys.argv[1] == "-group":
		groupname = sys.argv[2]
		for pupilIndex, pupilEntry in pupils.iterrows():
			if groupname in pupilEntry["Form"]:
				for contact in noNan(pupilEntry["Contacts"]).split(" "):
					contact = contact.strip()
					if not contact == "":
						inviteGuardian(pupilEntry["OldUsername"], contact)
