#!/usr/bin/python
import os
import re
import io
import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

usernames = pandas.read_csv(io.StringIO(dataLib.runCommand("gam print users query \"orgUnitPath='/KS-Pupils'\"")))
for usernamesIndex, usernamesValue in usernames.iterrows():
  usernameMatch = re.match("(.*\..*)(\d\d)@knightsbridgeschool.com", usernamesValue["primaryEmail"])
  if not usernameMatch == None:
    print(usernameMatch.group(1))
    print(usernameMatch.group(2))
