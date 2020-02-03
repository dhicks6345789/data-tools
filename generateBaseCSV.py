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

# Staff - previous output format:
# StaffID,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
staff = {"StaffID":[],"Title":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Username":[],"Identifier":[],"Form":[],"JobTitle":[]}
for currentStaffMember in iSAMSXML.findall("./HRManager/CurrentStaff/StaffMember"):
	if currentStaffMember.find("Surname").text == "Hicks":
		staff["StaffID"].append(currentStaffMember.find("UserCode").text)
		staff["Title"].append(currentStaffMember.find("Title").text)
		staff["GivenName"].append(currentStaffMember.find("PreferredName").text)
		staff["FamilyName"].append(currentStaffMember.find("Surname").text)
		staff["DateOfBirth"].append(currentStaffMember.find("DOB").text.split("T")[0])
		staff["Username"].append(currentStaffMember.find("SchoolEmailAddress").text.split("@")[0])
		staff["Identifier"].append(currentStaffMember.find("UserName").text)
		staff["Form"].append("")
		staff["JobTitle"].append("")
		
print(pandas.DataFrame(staff).to_csv(index=False))

# Output format:
# PupilID,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
pupils = {"PupilID":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Gender":[],"Username":[],"YearGroup":[],"Form":[],"Tutor":[]}
for currentPupil in iSAMSXML.findall("./PupilManager/CurrentPupils/Pupil"):
	if currentPupil.find("Surname").text == "Giles":
		print(currentPupil)

#installLib.writeFile(config["outputFolder"] + os.sep + "pupils.csv", pupils.to_csv(index=False))
print(pandas.DataFrame(pupils).to_csv(index=False))
