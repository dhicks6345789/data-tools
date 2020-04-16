#!/usr/bin/python
import os
import sys
import csv
import json
import installLib

requiredConfigParameters = ["dataFolder"]

def runCommand(theCommand):
	commandHandle = os.popen(theCommand)
	result = commandHandle.readlines()
	commandHandle.close()
	return result

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

emails = csv.DictReader(runCommand("gam user f.hall print messages query \"newer_than:4m AND from:no-reply@squarespace.com AND subject:'Knightsbridge School: A New Order has Arrived'\" max_to_print 100"))
header = next(emails)
for email in emails:
	print(email["id"])
