#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import random
import installLib

requiredConfigParameters = ["dataFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

def inviteGuardian(theUsername, theGuardian):
	os.system("gam create guardianinvite " + theGuardian + " " + theUsername + "@knightsbridgeschool.com")
		
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
				inviteGuardian(pupilEntry["OldUsername"], pupilEntry["MainContact"])
