#!/usr/bin/python
import os
import re
import sys
import csv
import json
import installLib

requiredConfigParameters = ["dataFolder"]

def readFile(theFilename):
	inHandle = open(theFilename)
	result = inHandle.read()
	inHandle.close()
	return result

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
for email in csv.DictReader(runCommand("gam user f.hall print messages query \"newer_than:4m AND from:no-reply@squarespace.com AND subject:'Knightsbridge School: A New Order has Arrived'\" max_to_print 150")):
	filenamePath = filenameRoot + os.sep + email["id"] + ".txt"
	if not os.path.exists(filenamePath):
		for emailWithBody in csv.DictReader(runCommand("gam user f.hall print messages ids " + email["id"] + " showbody")):
			installLib.writeFile(filenamePath, removeBlanks(emailWithBody["Body"]))

csvOutputHandle = open(config["dataFolder"] + os.sep + "Clubs" + os.sep + "clubsEmailsRawData.csv", 'w', newline='')
csvOutputWriter = csv.writer(csvOutputHandle, delimiter=",", quotechar="\"", quoting=csv.QUOTE_ALL)
csvOutputWriter.writerow(["orderNumber","orderDate","orderTime","parentName","parentEmail","itemDescription","itemCode","firstChildName","firstChildClass","secondChildName","secondChildClass"])
for emailFilePath in os.listdir(filenameRoot):
	orderNumber = ""
	orderDate = ""
	orderTime = ""
	parentName = ""
	parentEmail = ""
	itemDescription = ""
	itemCode = ""
	firstChildName = ""
	firstChildClass = ""
	secondChildName = ""
	secondChildClass = ""
	emailText = readFile(filenameRoot + os.sep + emailFilePath)
	matchResult = re.match(".*Order #(\d*?)\. Placed on (.*?) at (\d*?:\d*? ..).*", emailText, re.DOTALL)
	if not matchResult == None:
		orderNumber = matchResult[1].strip()
		orderDate = matchResult[2].strip()
		orderTime = matchResult[3].strip()
	matchResult = re.match(".*TO:\n(.*?)\n.*\n(.*?@.*?)\n.*ITEM.*", emailText, re.DOTALL)
	if not matchResult == None:
		parentName = matchResult[1].strip()
		parentEmail = matchResult[2].strip()
	matchResult = re.match(".*SUBTOTAL\n(.*?)\n(.*?)\n.*", emailText, re.DOTALL)
	if not matchResult == None:
		itemDescription = matchResult[1].strip()
		itemCode = matchResult[2].strip()
	matchResult = re.match(".*Name of your Child:\n(.*?)\nClass/Year:\n(.*?)\nName of Second Child:(.*?)\nClass/Year:\n(.*?)\n.*", emailText, re.DOTALL)
	if not matchResult == None:
		firstChildName = matchResult[1].strip()
		firstChildClass = matchResult[2].strip()
		secondChildName = matchResult[3].strip()
		secondChildClass = matchResult[4].strip()
		csvOutputWriter.writerow([orderNumber,orderDate,orderTime,parentName,parentEmail,itemDescription,itemCode,firstChildName,firstChildClass,secondChildName,secondChildClass])
