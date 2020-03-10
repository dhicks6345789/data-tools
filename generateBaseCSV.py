#!/usr/bin/python
import os
import sys
import json
import pandas
import installLib
import xml.etree.ElementTree

requiredConfigParameters = ["dataFolder"]

def normaliseName(theName):
	return theName.strip().replace("\\","")

def normaliseUserName(theName):
	return theName.strip().lower().replace(" ","").replace("-","").replace("\\","")

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
staff = {"GUID":[],"ID":[],"UserCode":[],"Title":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Username":[],"Identifier":[],"Form":[],"JobTitle":[]}
for currentStaffMember in iSAMSXML.findall("./HRManager/CurrentStaff/StaffMember"):
	staff["GUID"].append(currentStaffMember.attrib["PersonGuid"])
	staff["ID"].append(currentStaffMember.attrib["Id"])
	staff["UserCode"].append(currentStaffMember.find("UserCode").text)
	staff["Title"].append(currentStaffMember.find("Title").text)
	staff["GivenName"].append(normaliseName(currentStaffMember.find("PreferredName").text))
	staff["FamilyName"].append(normaliseName(currentStaffMember.find("Surname").text))
	staff["DateOfBirth"].append(getValue(currentStaffMember, "DOB").split("T")[0])
	staff["Username"].append(getValue(currentStaffMember, "SchoolEmailAddress").split("@")[0])
	staff["Identifier"].append(getValue(currentStaffMember, "Username"))
	staff["Form"].append("")
	staff["JobTitle"].append("")
installLib.writeFile(config["dataFolder"] + os.sep + "staff.csv", pandas.DataFrame(staff).to_csv(index=False))

forms = {}
# Pupils - previous output format:
# PupilID,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
pupils = {"GUID":[],"ID":[],"UserCode":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Gender":[],"Username":[],"OldUsername":[],"YearGroup":[],"Form":[],"Tutor":[]}
for currentPupil in iSAMSXML.findall("./PupilManager/CurrentPupils/Pupil"):
	pupils["GUID"].append(currentPupil.attrib["PersonGuid"])
	pupils["ID"].append(currentPupil.attrib["Id"])
	pupils["UserCode"].append(getValue(currentPupil, "UserCode"))
	pupils["GivenName"].append(normaliseName(currentPupil.find("Preferredname").text))
	pupils["FamilyName"].append(normaliseName(currentPupil.find("Surname").text))
	pupils["DateOfBirth"].append(currentPupil.find("DOB").text.split("T")[0])
	pupils["Gender"].append(currentPupil.find("Gender").text)
	pupils["Username"].append(currentPupil.find("EmailAddress").text.split("@")[0])
	
	oldUsername = "ks" + normaliseUserName(currentPupil.find("Surname").text)[:4]
	oldUsername = oldUsername + normaliseUserName(currentPupil.find("Preferredname").text)[:3]
	oldUsername = oldUsername + normaliseUserName(currentPupil.find("EmailAddress").text).split("@")[0][-2:]
	pupils["OldUsername"].append(oldUsername)
	
	pupils["YearGroup"].append(currentPupil.find("EmailAddress").text.split("@")[0][-2:])
	pupils["Form"].append(currentPupil.find("Form").text)
	forms[currentPupil.find("Form").text] = 1
	pupils["Tutor"].append(getValue(currentPupil, "Tutor"))
installLib.writeFile(config["dataFolder"] + os.sep + "pupils.csv", pandas.DataFrame(pupils).to_csv(index=False))

installLib.writeFile(config["dataFolder"] + os.sep + "forms.csv", sorted(forms.keys()))
