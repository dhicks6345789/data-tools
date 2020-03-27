#!/usr/bin/python
import os
import sys
import json
import pandas
import installLib
import xml.etree.ElementTree

requiredConfigParameters = ["dataFolder"]

def normaliseName(theName):
	return theName.strip().replace("\\","").replace("(","").replace(")","")

def normaliseUserName(theName):
	return normaliseName(theName).lower().replace(" ","").replace("-","").replace("'","")

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
staff = {"GUID":[],"ID":[],"UserCode":[],"Title":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Username":[],"Identifier":[],"Form":[],"Role":[],"JobTitle":[],"TelephoneNumber":[]}
for currentStaffMember in iSAMSXML.findall("./HRManager/CurrentStaff/StaffMember"):
	username = getValue(currentStaffMember, "SchoolEmailAddress").split("@")[0].lower().strip()
	if not username == "":
		staff["GUID"].append(currentStaffMember.attrib["PersonGuid"])
		staff["ID"].append(currentStaffMember.attrib["Id"])
		staff["UserCode"].append(currentStaffMember.find("UserCode").text)
		staff["Title"].append(currentStaffMember.find("Title").text)
		staff["GivenName"].append(normaliseName(currentStaffMember.find("PreferredName").text))
		staff["FamilyName"].append(normaliseName(currentStaffMember.find("Surname").text))
		staff["DateOfBirth"].append(getValue(currentStaffMember, "DOB").split("T")[0])
		staff["Username"].append(username)
		staff["Identifier"].append(getValue(currentStaffMember, "Username"))
		staff["Form"].append("")
		roleName = ""
		roles = currentStaffMember.find("Roles")
		if not roles == None:
			for role in roles:
				roleName = role.find("Name").text.strip()
				if "-" in roleName:
					roleName = roleName.split("-")[1].strip()
		staff["Role"].append(roleName)
		staff["JobTitle"].append("")
		staff["TelephoneNumber"].append("")
installLib.writeFile(config["dataFolder"] + os.sep + "staff.csv", pandas.DataFrame(staff).to_csv(index=False))

forms = {}
# Pupils - previous output format:
# PupilID,GivenName,FamilyName,DateOfBirth,Gender,Username,YearGroup,Form,Tutor
pupils = {"GUID":[],"ID":[],"UserCode":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Gender":[],"Username":[],"OldUsername":[],"YearGroup":[],"Form":[],"Tutor":[],"Contacts":[]}
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
	pupils["Contacts"].append("")
	
# Possible relationships:
validRalationships = ["guardian", "mother", "father", "stepmother", "stepfather", "parent", "security", "nanny", "au pair", "babysitter", "tutor", "childminder", "aunt", "uncle", "pa", "grandmother", "grandfather", "godmother", "godfather", "sister", "brother", "cousin", "other family member", "friend", "contact", "company", "personal"]
relationshipsMap = {"mother_copy":"mother", "father_copy":"father", "family friend":"friend", "pa (harry)":"pa", "pa to parent":"pa", "step mother":"step mother", "step-mother":"step mother", "step father":"step father", "step-father":"step father", "other contact":"contact", "parents_copy":"parent"}
# .strip().lower()...
relationships = {}
pupilsDataFrame = pandas.DataFrame(pupils)
for contact in iSAMSXML.findall("./PupilManager/Contacts/Contact"):
	contactEmailAddress = contact.find("EmailAddress")
	if not contactEmailAddress == None and not contactEmailAddress.text == None and contact.attrib["IsFirstPersonContact"] == "True":
		relationships[contact.find("RelationshipRaw").text] = 1
		for contactPupil in contact.find("Pupils"):
			pupilID = contactPupil.attrib["Id"]
			for pupilIndex, pupil in pupilsDataFrame.iterrows():
				if pupil["ID"] == pupilID:
					contactsRecord = pupilsDataFrame.at[pupilIndex, "Contacts"]
					if contactsRecord == "":
						contactsRecord = contactEmailAddress.text.strip()
					elif not contactEmailAddress.text.strip() in contactsRecord:
						contactsRecord = contactsRecord + " " + contactEmailAddress.text.strip()
					pupilsDataFrame.at[pupilIndex, "Contacts"] = contactsRecord
installLib.writeFile(config["dataFolder"] + os.sep + "pupils.csv", pupilsDataFrame.to_csv(index=False))

print(relationships.keys())

installLib.writeFile(config["dataFolder"] + os.sep + "forms.csv", sorted(forms.keys()))
