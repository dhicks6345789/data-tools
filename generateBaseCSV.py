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
	if currentStaffMember.find("Surname").text == "Hicks":
		print(currentStaffMember.find("UserCode").text)
		print(currentStaffMember.find("PreferredName").text)
		print(currentStaffMember.find("Surname").text)
		print(currentStaffMember.find("DOB").text.split("T")[0])
		print(currentStaffMember.find("Gender").text)
		print(currentStaffMember.find("UserName").text)
		for currentStaffMemberAttribute in currentStaffMember:
			print(currentStaffMemberAttribute.tag, currentStaffMemberAttribute.text)
			#PreviousMISId {}
			#Initials {}
			#UserCode {}
			#UserName {}
			#Title {}
			#Forename {}
			#MiddleNames {}
			#Surname {}
			#FullName {}
			#NameInitials {}
			#PreferredName {}
			#Salutation {}
			#DOB {}
			#Gender {}
			#SchoolEmailAddress {}
			#SchoolMobileNumber {}
			#PersonalMobileNumber {}
			#TeachingStaff {}
			#Divisions {}
			#Roles {}

# Output format:
# PupilID,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
pupils = pandas.DataFrame({"PupilID":[],"GivenName":[]})
installLib.writeFile(config["outputFolder"] + os.sep + "pupils.csv", pupils.to_csv())
