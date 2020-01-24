#!/usr/bin/python
import sys
import json
import installLib

requiredConfigParameters = ["pupilsCSVInputFile", "outputFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

print(config["pupilsCSVInputFile"])
print(config["outputFolder"] + "\\Scout\\allUsersForBorrowerImport.csv")

print("P1949,kskirkoli15,Student,Library,OPAC Only,Pupils,Olivia,Kirkup,S5C,28/01/2009")

pupils = open(config["pupilsCSVInputFile"])
pupilsReader = pupils.reader(pupils, delimiter=',')
for pupilRow in pupilsReader:
	print(pupilRow)
