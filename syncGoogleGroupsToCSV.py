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
		
# Read the existing basic groups data.
groups = pandas.read_csv(config["dataFolder"] + os.sep + "groups.csv", header=0)
for groupIndex, group in groups.iterrows():
	print(group["Members"])

# Create a CSV file for each group (i.e. Year Group or Form).
#os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
#print("gam update group " + groupDetails[group]["email"].lower() + " sync member file \"" + config["dataFolder"] + os.sep + "Groups" + os.sep + group + ".csv\" 2>&1")
