#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

# Set up yeargroups.
groupDetails = {
  "KS-SEC-PUPILS-NURSERY":{"Email":"nurserypupils@knightsbridgeschool.com","Form":"Lions"},
  "KS-SEC-PUPILS-RECEPTION":{"Email":"receptionpupils@knightsbridgeschool.com","Form":"Rec"},
  "KS-SEC-PUPILS-J1":{"Email":"j1pupils@knightsbridgeschool.com","Form":"1"},
  "KS-SEC-PUPILS-J2":{"Email":"j2pupils@knightsbridgeschool.com","Form":"2"},
  "KS-SEC-PUPILS-J3":{"Email":"j3pupils@knightsbridgeschool.com","Form":"3"},
  "KS-SEC-PUPILS-S4":{"Email":"s4pupils@knightsbridgeschool.com","Form":"4"},
  "KS-SEC-PUPILS-S5":{"Email":"s5pupils@knightsbridgeschool.com","Form":"5"},
  "KS-SEC-PUPILS-S6":{"Email":"s6pupils@knightsbridgeschool.com","Form":"6"},
  "KS-SEC-PUPILS-S7":{"Email":"s7pupils@knightsbridgeschool.com","Form":"7"},
  "KS-SEC-PUPILS-S8":{"Email":"s8pupils@knightsbridgeschool.com","Form":"8"}
}

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
  if not requiredConfigParameter in config.keys():
    print("Error - required value " + requiredConfigParameter + " not set in config.json.")
    sys.exit(1)

# Input data headings:
# Pupils: GUID,UserCode,GivenName,FamilyName,DateOfBirth,Gender,Username,OldUsername,YearGroup,Form,Tutor
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,JobTitle
# Output format (for Google Groups upload):
# Group Email [Required],Member Email,Member Type,Member Role

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Get a list of forms (excluding Nursery and Year 7 and 8, as they only have the one class).
forms={}
for pupilIndex, pupil in pupils.iterrows():
  for yearGroup in ["Rec","1","2","3","4","5","6"]:
    if yearGroup in pupil["Form"]:
      forms[pupil["Form"]] = 1

# Set up to create a CSV file for each form.
for form in forms.keys():
  groupDetails["KS-SEC-PUPILS-" + form] = {"Email":form + "pupils@knightsbridgeschool.com","Form":form}

# Create a CSV file for each group (i.e. Year Group or Form).
#os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
#for group in groupDetails.keys():
#  print("Syncing members and generating CSV file for group " + group + " (" + groupDetails[group]["Email"].lower() + ")...")
#  infoResult = installLib.runCommand("gam info group " + groupDetails[group]["Email"].lower() + " 2>&1")
#  currentMembers = []
#  if infoResult[0].strip().endswith("Does not exist"):
#    os.system("gam create group " + groupDetails[group]["Email"].lower() + " name " + group + " description \"All members of " + group + "\" who_can_join all_in_domain_can_join who_can_post_message all_members_can_post who_can_view_membership all_managers_can_view allow_external_members false who_can_invite none_can_invite 2>&1")
#  else:
#    os.system("gam update group " + groupDetails[group]["Email"].lower() + " name " + group + " description \"All members of " + group + "\" who_can_join all_in_domain_can_join who_can_post_message all_members_can_post who_can_view_membership all_managers_can_view allow_external_members false who_can_invite none_can_invite 2>&1")
#    for infoLine in infoResult:
#      if infoLine.strip().startswith("member:"):
#        currentMembers.append(infoLine.strip().split(" ")[1])
#  futureMembers = []
#  outputString = "Group Email [Required],Member Email [Required],Member Type,Member Role\n"
#  for pupilIndex, pupil in pupils.iterrows():
#    if not re.match(".*" + groupDetails[group]["Form"] + ".*", pupil["Form"]) == None:
#      futureMembers.append(pupil["OldUsername"] + "@knightsbridgeschool.com")
#      outputString = outputString + groupDetails[group]["Email"].lower() + "," + pupil["OldUsername"] + "@knightsbridgeschool.com,USER,MEMBER\n"
#  installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv", outputString)
#  for futureMember in futureMembers:
#    if not futureMember in currentMembers:
#      os.system("gam update group " + groupDetails[group]["Email"].lower() + " add member " + futureMember + " 2>&1")
#  for currentMember in currentMembers:
#    if not currentMember in futureMembers:
#      os.system("gam update group " + groupDetails[group]["Email"].lower() + " remove user " + currentMember + " 2>&1")
#  os.system("gam update group " + groupDetails[group]["Email"].lower() + " add manager user j.croxford@knightsbridgeschool.com 2>&1")
	
# Read the existing basic staff details.
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)
outputString = "Group Email [Required],Member Email [Required],Member Type,Member Role\n"
for staffIndex, staff in staff.iterrows():
  outputString = outputString + "staff@knightsbridgeschool.com," + staff["username"] + "@knightsbridgeschool.com,USER,MEMBER\n"
installLib.writeFile(config["dataFolder"] + os.sep + "Groups" + os.sep + "staff.csv", outputString)
