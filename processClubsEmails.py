#!/usr/bin/python
import os
import re
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

def removeBlanks(theString):
	result = ""
	for line in theString.split("\n"):
		line = line.strip()
		if not line == "":
			result = result + line + "\n"
	return result.strip()

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

os.makedirs(config["dataFolder"] + os.sep + "Clubs", exist_ok=True)
os.makedirs(config["dataFolder"] + os.sep + "Clubs" + os.sep + "Emails", exist_ok=True)

filenameRoot = config["dataFolder"] + os.sep + "Clubs" + os.sep + "Emails"
for email in csv.DictReader(runCommand("gam user f.hall print messages query \"newer_than:4m AND from:no-reply@squarespace.com AND subject:'Knightsbridge School: A New Order has Arrived'\" max_to_print 5")):
	filenamePath = filenameRoot + os.sep + email["id"] + ".txt"
	if not os.path.exists(filenamePath):
		for emailWithBody in csv.DictReader(runCommand("gam user f.hall print messages ids " + email["id"] + " showbody")):
			installLib.writeFile(filenamePath, removeBlanks(emailWithBody["Body"]))
for emailFilePath in os.listdir(filenameRoot):
	orderNumber = ""
	orderDate = ""
	emailText = str(installLib.readFile(filenameRoot + os.sep + emailFilePath))
	#Order #02248. Placed on January 27, 2020 at 3:56 PM GMT
	matchResult = re.match(".*Order #(\d*?)\..*", emailText)
	if not matchResult == None:
		orderNumber = matchResult[1]
	print(orderNumber)
