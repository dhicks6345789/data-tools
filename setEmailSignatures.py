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
# Staff: GUID,UserCode,Title,GivenName,FamilyName,DateOfBirth,Username,Identifier,Form,Role,JobTitle,TelephoneNumber
staff = pandas.read_csv(config["dataFolder"] + os.sep + "staff.csv", header=0)

# Note: staff job title and telephone number values are set in a separate script from generateBaseCSV.py and from this script to aid
# testing and debugging.
outputString = ""
for staffIndex, staffMember in staff.iterrows():
  # gam user [signature <signature text>] [file <signature file>] [replyto <EmailAddress>] (replace <Tag> <String>)*
  if staff["Username"] == "d.hicks":
    print("gam user " + staff["Username"] + "@knightsbridgeschool.com signature file config/emailSignature.html replyto " + staff["Username"] + "@knightsbridgeschool.com replace email \"" + staff["Username"] + "@knightsbridgeschool.com replace name \"" + staff["GivenName"] + " " + staff["FamilyName"] + "\" replace title \"" + staff["JobTitle"] + "\"")
