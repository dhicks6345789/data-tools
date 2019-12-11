#!/usr/bin/python
import json
import installLib

requiredConfigParameters = ["iSAMSAPIKey"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)
    
# Code goes here - more stuff.
print(config["iSAMSAPIKey"])
