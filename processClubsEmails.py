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

os.makedirs(config["dataFolder"] + os.sep + "Clubs", exist_ok=True)
os.makedirs(config["dataFolder"] + os.sep + "Clubs" + os.sep + "Emails", exist_ok=True)

for email in csv.DictReader(runCommand("gam user f.hall print messages query \"newer_than:4m AND from:no-reply@squarespace.com AND subject:'Knightsbridge School: A New Order has Arrived'\" max_to_print 5")):
	filenamePath = config["dataFolder"] + os.sep + "Clubs" + os.sep + "Emails" + os.sep + email["id"] + ".txt"
	if not os.path.exists(filenamePath):
		for emailWithBody in csv.DictReader(runCommand("gam user f.hall print messages ids " + email["id"] + " showbody")):
			installLib.writeFile(filenamePath, emailWithBody["Body"])
