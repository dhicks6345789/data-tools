#!/usr/bin/python
import os
import sys
import json
import pandas
import installLib
import xml.etree.ElementTree

requiredConfigParameters = ["outputFolder"]

def getValue(theXMLNode, theTag):
	findResult = theXMLNode.find(theTag) 
	if findResult == None:
		return ""
	return findResult.text

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

iSAMSXML = xml.etree.ElementTree.fromstring(installLib.readFile("iSAMSData.xml"))

# Staff - previous output format:
# StaffID,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
staff = {"StaffID":[],"Title":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Username":[],"Identifier":[],"Form":[],"JobTitle":[]}
for currentStaffMember in iSAMSXML.findall("./HRManager/CurrentStaff/StaffMember"):
	staff["StaffID"].append(currentStaffMember.find("UserCode").text)
	staff["Title"].append(currentStaffMember.find("Title").text)
	staff["GivenName"].append(currentStaffMember.find("PreferredName").text)
	staff["FamilyName"].append(currentStaffMember.find("Surname").text)
	staff["DateOfBirth"].append(currentStaffMember.find("DOB").text.split("T")[0])
	staff["Username"].append(getValue(currentStaffMember, "SchoolEmailAddress").split("@")[0])
	staff["Identifier"].append(getValue(currentStaffMember, "Username"))
	staff["Form"].append("")
	staff["JobTitle"].append("")
installLib.writeFile(config["outputFolder"] + os.sep + "pupils.csv", pandas.DataFrame(staff).to_csv(index=False))

# Pupils - previous output format:
# PupilID,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
pupils = {"PupilID":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Gender":[],"Username":[],"YearGroup":[],"Form":[],"Tutor":[]}
for currentPupil in iSAMSXML.findall("./PupilManager/CurrentPupils/Pupil"):
	pupils["PupilID"].append(getValue(currentPupil, "UserCode"))
	pupils["GivenName"].append(currentPupil.find("Preferredname").text)
	pupils["FamilyName"].append(currentPupil.find("Surname").text)
	pupils["DateOfBirth"].append(currentPupil.find("DOB").text.split("T")[0])
	pupils["Gender"].append(currentPupil.find("Gender").text)
	pupils["Username"].append(currentPupil.find("EmailAddress").text.split("@")[0])
	pupils["YearGroup"].append(currentPupil.find("EmailAddress").text.split("@")[0][-2:])
	pupils["Form"].append(currentPupil.find("Form").text)
	pupils["Tutor"].append(getValue(currentPupil, "Tutor"))
installLib.writeFile(config["outputFolder"] + os.sep + "pupils.csv", pandas.DataFrame(pupils).to_csv(index=False))
