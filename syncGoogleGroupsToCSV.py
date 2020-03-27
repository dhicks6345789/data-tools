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

# Create a CSV file for each GSuite group.
os.makedirs(config["dataFolder"] + os.sep + "Groups", exist_ok=True)
print("erase " + config["dataFolder"] + os.sep + "Groups" + os.sep + "*.*")
for groupIndex, group in groups.iterrows():
	outputString = ""
	for member in str(group["Members"]).split():
		outputString = outputString + member + ",\n"
	print(outputString)
