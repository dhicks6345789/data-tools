#!/usr/bin/python
import os
import ssl
import json
import installLib
import urllib.request

requiredConfigParameters = ["iSAMSAPIKey", "iSAMSAPIDomain"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)
    
# Go and get the data from the iSAMS API.
print("Getting data from iSAMS.")
response = urllib.request.urlopen("https://" + config["iSAMSAPIDomain"] + "/api/batch/1.0/xml.ashx?apiKey=" + config["iSAMSAPIKey"], context=ssl._create_unverified_context())
installLib.writeFile("iSAMSData.xml", str(response.read())[2:-1])

# Get a list of all courses, output in CSV format directly from GAM.
print("Getting course list from Google Classroom.")
os.system("gam print courses > \"" + config["dataFolder"] + os.sep + "courses.csv\"")
