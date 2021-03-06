#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import installLib

requiredConfigParameters = ["dataFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
  if not requiredConfigParameter in config.keys():
    print("Error - required value " + requiredConfigParameter + " not set in config.json.")
    sys.exit(1)
    
# Read the existing basic staff details. Headings:
# GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,Role,JobTitle,TelephoneNumber
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)
# Tell Pandas that the (currently empty) JobTitle and TelephoneNumber columns are actually meant to be String, not Float.
staff["JobTitle"] = staff["JobTitle"].astype(str)
staff["TelephoneNumber"] = staff["TelephoneNumber"].astype(str)

# Staff job titles: not recorded by iSAMS, but instead set manually in GSuite for each signature. Therefore, for each user,
# retrive the existing signature and extract the "job title" value, updating the "staff" records read from CSV above. Use the job
# Role if no other value is present, then write out the updated "staff.csv" again with the added values.
outputString = ""
for staffIndex, staffMember in staff.iterrows():
  print("Adding details for staff member " + staffMember["GivenName"] + " " + staffMember["FamilyName"])
  if staff.at[staffIndex, "JobTitle"] == "nan":
    staff.at[staffIndex, "JobTitle"] = ""
  if staff.at[staffIndex, "TelephoneNumber"] == "nan":
    staff.at[staffIndex, "TelephoneNumber"] = ""
  staffName = ""
  staffJobTitle = ""
  staffUsername = ""
  staffTelephone = ""
  for sigLine in installLib.runCommand("gam user " + staffMember["Username"] + " show signature"):
    matchResult = re.match(".*bold..(.*)..span. \| (.*)..div..*", sigLine.strip())
    if not matchResult == None:
      staffName = matchResult[1].strip()
      staffJobTitle = matchResult[2].strip().replace("&amp;", "&")
    matchResult = re.match(".*blank..(.*)@knightsbridgeschool.com./a..*", sigLine.strip())
    if not matchResult == None:
      staffUsername = matchResult[1]
    matchResult = re.match("([ \d]*)</div>$", sigLine.strip())
    if not matchResult == None:
      if not matchResult[1] == "":
        staffTelephone = matchResult[1]
  if staffUsername == "":
    staffUsername = staffMember["Username"]
  if staffTelephone == "":
    staffTelephone = "020 7590 9000"
  if staffJobTitle == "":
    staffJobTitle = staffMember["Role"]
  if not staffMember["Username"] == staffUsername:
    print("Username mismatch: " + staffMember["Username"] + " not equal to " + staffUsername)
  else:
    staff.at[staffIndex, "JobTitle"] = staffJobTitle
    staff.at[staffIndex, "TelephoneNumber"] = staffTelephone
installLib.writeFile(config["dataFolder"] + os.sep + "staff.csv", staff.to_csv(index=False))
