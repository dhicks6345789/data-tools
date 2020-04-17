#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import dataLib

requiredConfigParameters = ["dataFolder"]

clubsRoot = dataLib.config["dataFolder"] + os.sep + "Clubs"
os.makedirs(clubsRoot, exist_ok=True)
emailsRoot = clubsRoot + os.sep + "Emails"
os.makedirs(emailsRoot, exist_ok=True)

pandas.read_excel(clubsRoot + os.sep + "options.xlsx")
sys.exit(0)

for email in csv.DictReader(runCommand("gam user f.hall print messages query \"newer_than:6m AND from:no-reply@squarespace.com AND subject:'Knightsbridge School: A New Order has Arrived'\"").split("\n")):
	filenamePath = filenameRoot + os.sep + email["id"] + ".txt"
	if not os.path.exists(filenamePath):
		for emailWithBody in csv.DictReader(runCommand("gam user f.hall print messages ids " + email["id"] + " showbody").split("\n)):
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
		if not matchResult[4].startswith("blog <"):
			secondChildClass = matchResult[4].strip()
		csvOutputWriter.writerow([orderNumber,orderDate,orderTime,parentName,parentEmail,itemDescription,itemCode,firstChildName,firstChildClass,secondChildName,secondChildClass])
