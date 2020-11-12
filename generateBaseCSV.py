#!/usr/bin/python
import os
import sys
import json
import pandas
import installLib
import xml.etree.ElementTree

requiredConfigParameters = ["dataFolder"]

# Define a list of relationships a pupil can have with a contact, ordered by importance for use as a primary contact.
validRelationships = ["guardian", "parent", "mother", "father", "stepmother", "stepfather", "security", "nanny", "au pair", "babysitter", "tutor", "childminder", "aunt", "uncle", "pa", "grandmother", "grandfather", "godmother", "godfather", "sister", "brother", "cousin", "other family member", "friend", "contact", "company", "personal"]
mainRelationships = ["parent", "mother", "father"]

# A map and function to regularise some of the data coming out of the "relationship" field.
relationshipsMap = {"mother_copy":"mother", "father_copy":"father", "family friend":"friend", "pa (harry)":"pa", "pa to parent":"pa", "step mother":"step mother", "step-mother":"step mother", "step father":"step father", "step-father":"step father", "other contact":"contact", "parents_copy":"parent", "parents":"parent"}
def normaliseRelationship(theRelationship):
	result = theRelationship
	for item in relationshipsMap.keys():
		result = result.replace(item, relationshipsMap[item])
	return result

def normaliseName(theName):
	return theName.strip().replace("\\","").replace("(","").replace(")","")

def normaliseUserName(theName):
	return normaliseName(theName).lower().replace(" ","").replace("-","").replace("'","")

def multisplit(theString, theSplit):
	result = theString.split(theSplit[0])
	for pl in range(1, len(theSplit)):
		tempResult = []
		for resultItem in result:
			for splitItem in resultItem.split(theSplit[pl]):
				tempResult.append(splitItem.strip())
		result = tempResult
	return result

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

# Get a list of Yeargroups / Form / Teaching Sets from iSAMS.
for currentSet in iSAMSXML.findall("./TeachingManager/Sets/Set"):
	print(currentSet.find("SetCode").text)
	
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

print("Generating the base pupils.csv file...")
forms = {}
houses = {}
pupils = {"GUID":[],"ID":[],"UserCode":[],"GivenName":[],"FamilyName":[],"DateOfBirth":[],"Gender":[],"Username":[],"OldUsername":[],"YearGroup":[],"Form":[],"House":[],"Tutor":[],"Contacts":[]}
for currentPupil in iSAMSXML.findall("./PupilManager/CurrentPupils/Pupil"):
	if currentPupil.find("Preferredname") == None:
		print("ERROR: Pupil record with no name:")
		for pupilField in currentPupil.keys():
			print(" - " + pupilField + ": " + currentPupil.attrib[pupilField])
	else:
		pupils["GUID"].append(currentPupil.attrib["PersonGuid"])
		pupils["ID"].append(currentPupil.attrib["Id"])
		pupils["UserCode"].append(getValue(currentPupil, "UserCode"))
		pupils["GivenName"].append(normaliseName(currentPupil.find("Preferredname").text))
		pupils["FamilyName"].append(normaliseName(currentPupil.find("Surname").text))
		pupils["DateOfBirth"].append(currentPupil.find("DOB").text.split("T")[0])
		pupils["Gender"].append(currentPupil.find("Gender").text)
		pupilEmail = currentPupil.find("EmailAddress")
		if pupilEmail == None:
			pupils["Username"].append("")
			pupils["OldUsername"].append("")
			pupils["YearGroup"].append("")
		else:
			pupils["Username"].append(pupilEmail.text.split("@")[0])
		
			oldUsername = "ks" + normaliseUserName(currentPupil.find("Surname").text)[:4]
			oldUsername = oldUsername + normaliseUserName(currentPupil.find("Preferredname").text)[:3]
			oldUsername = oldUsername + normaliseUserName(currentPupil.find("EmailAddress").text).split("@")[0][-2:]
			pupils["OldUsername"].append(oldUsername)
	
			pupils["YearGroup"].append(currentPupil.find("EmailAddress").text.split("@")[0][-2:])
		
		pupils["Form"].append(currentPupil.find("Form").text)
		forms[currentPupil.find("Form").text] = 1
		if currentPupil.find("AcademicHouse") == None:
			print("Pupil " + currentPupil.find("Preferredname").text + " " + currentPupil.find("Surname").text + " has no House set.")
			house = ""
		else:
			house = currentPupil.find("AcademicHouse").text
			houses[house] = 1
		pupils["House"].append(house)
		pupils["Tutor"].append(getValue(currentPupil, "Tutor"))
		pupils["Contacts"].append("")
pupilsDataFrame = pandas.DataFrame(pupils)

print("Adding pupil contact information to pupils.csv...")
# Extract each pupil contact and their relationship with the pupil. Only keep a contact if their relationship with the pupil is in the agreed
# list (parent / guardian or nanny) and if that contact is listed as being available for correspondance.
for contact in iSAMSXML.findall("./PupilManager/Contacts/Contact"):
	contactEmailAddress = contact.find("EmailAddress")
	if not contactEmailAddress == None and not contactEmailAddress.text == None and (contact.find("CorrespondenceMailMerge").text == "1" or contact.find("MailMergeAll").text == "1") and normaliseRelationship(contact.find("RelationshipRaw").text.strip().lower()) in mainRelationships:
		for contactPupil in contact.find("Pupils"):
			for pupilIndex, pupil in pupilsDataFrame.iterrows():
				for contactEmailAddressValue in multisplit(contactEmailAddress.text.strip(), " ;"):
					if pupil["ID"] == contactPupil.attrib["Id"] and contactEmailAddressValue not in pupilsDataFrame.at[pupilIndex, "Contacts"]:
						pupilsDataFrame.at[pupilIndex, "Contacts"] = (pupilsDataFrame.at[pupilIndex, "Contacts"] + " " + contactEmailAddressValue).strip()

# Write out pupils.csv.
installLib.writeFile(config["dataFolder"] + os.sep + "pupils.csv", pupilsDataFrame.to_csv(index=False))

# Write out forms.csv.
installLib.writeFile(config["dataFolder"] + os.sep + "forms.csv", sorted(forms.keys()))

# Write out houses.csv.
installLib.writeFile(config["dataFolder"] + os.sep + "houses.csv", sorted(houses.keys()))
