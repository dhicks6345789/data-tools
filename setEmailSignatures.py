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

# Input data headings:
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,Role,JobTitle

# Read the existing basic staff details.
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)
# Tell Pandas that the (currently empty) JobTitle and TelephoneNumber columns are actually meant to be String, not Float.
staff["JobTitle"] = staff["JobTitle"].astype(str)
staff["TelephoneNumber"] = staff["TelephoneNumber"].astype(str)

# Staff job titles: not recorded by iSAMS, but instead set manually in GSuite for each signature. Therefore, for each user, first
# retrive the existing signature and extract the "job title" value, updating the "staff" records reqd from CSV above. Use the job
# Role if no other value is present, then write out the updated "staff.csv" again with the added values.
outputString = ""
for staffIndex, staffMember in staff.iterrows():
  if staff.at[staffIndex, "JobTitle"] == "nan":
    staff.at[staffIndex, "JobTitle"] = ""
  if staff.at[staffIndex, "TelephoneNumber"] == "nan":
    staff.at[staffIndex, "TelephoneNumber"] = ""
  # gam user [signature <signature text>] [file <signature file>] [replyto <EmailAddress>] (replace <Tag> <String>)*
  staffName = ""
  staffJobTitle = ""
  staffUsername = ""
  staffTelephone = ""
  for sigLine in installLib.runCommand("gam user " + staffMember["Username"] + " show signature"):
    matchResult = re.match(".*bold..(.*)..span. \| (.*)..div..*", sigLine.strip())
    if not matchResult == None:
      staffName = matchResult[1]
      staffJobTitle = matchResult[2]
    matchResult = re.match(".*blank..(.*)@knightsbridgeschool.com./a..*", sigLine.strip())
    if not matchResult == None:
      staffUsername = matchResult[1]
    matchResult = re.match("([ \d]*)</div>$", sigLine.strip())
    if not matchResult == None:
      if not matchResult[1] == "":
        staffTelephone = matchResult[1]
  if not staffMember["Username"] == staffUsername:
    print("Username mismatch: " + staffMember["Username"] + " not equal to " + staffUsername)
  else:
    staff.at[staffIndex, "JobTitle"] = staffJobTitle
installLib.writeFile(config["dataFolder"] + os.sep + "staff.csv", staff.to_csv(index=False))
#  if staff["Username"] == "d.hicks":
#    print("gam user " + staff["Username"] + "@knightsbridgeschool.com signature file config/emailSignature.html replyto " + staff["Username"] + "@knightsbridgeschool.com replace name \"" + staff["GivenName"] + " " + staff["FamilyName"] + "\" replace role \"" + staff["Role"] + "\"")
