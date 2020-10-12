#!/usr/bin/python
import os
import re
import io
import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

#usernames = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print users query \"orgUnitPath='/KS-Pupils'\" ou")))
usernames = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print users query \"orgUnitPath='/'\" ou")))
for usernamesIndex, usernamesValue in usernames.iterrows():
  usernameMatch = re.match("(.*\..*)(\d\d)@knightsbridgeschool.com", usernamesValue["primaryEmail"])
  if not usernameMatch == None:
    if not usernamesValue["orgUnitPath"] == "/KS-Pupils/" + usernameMatch.group(2):
      print("Moving user " + usernameMatch.group(1) + usernameMatch.group(2) + " to /KS-Pupils/" + usernameMatch.group(2))
      #os.system("gam update user " + usernameMatch.group(1) + usernameMatch.group(2) + " ou /KS-Pupils/" + usernameMatch.group(2))
