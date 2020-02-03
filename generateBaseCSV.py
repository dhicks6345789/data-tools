#!/usr/bin/python
import os
import sys
import json
import pandas
import installLib
import xml.etree.ElementTree

requiredConfigParameters = ["outputFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

iSAMSXML = xml.etree.ElementTree.fromstring(installLib.readFile("iSAMSData.xml"))
for currentStaffMember in iSAMSXML.findall("./HRManager/CurrentStaff/StaffMember"):
	print(currentStaffMember.tag)
	
# Output format:
# PupilID,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
pupils = pandas.DataFrame({"PupilID":[],"GivenName":[]})
installLib.writeFile(config["outputFolder"] + os.sep + "pupils.csv", pupils.to_csv())
