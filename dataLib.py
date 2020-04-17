#!/usr/bin/python
import os
import json

# A set of utility functions to help with general data manipulation.

# Reads the given file, returns the entire contents as a single string.
def readFile(theFilename):
	inHandle = open(theFilename)
	result = inHandle.read()
	inHandle.close()
	return result

# Runs the given command, returns the entire output as a single string.
def runCommand(theCommand):
	commandHandle = os.popen(theCommand)
	result = commandHandle.read()
	commandHandle.close()
	return result

# Takes the given string and returns a copy with any blank lines removed, also removes any whitespace and the start and end of each line.
def removeBlanks(theString):
	result = ""
	for line in theString.split("\n"):
		line = line.strip()
		if not line == "":
			result = result + line + "\n"
	return result.strip()

# Takes an array of strings, then checks the JSON config file to make sure the required parameters are indeed set.
# Returns an array of configuration values.
loadConfig(requiredConfigParameters):
	# Load the configuration file.
	config = json.loads(readFile("config/config.json"))
	for requiredConfigParameter in requiredConfigParameters:
		if not requiredConfigParameter in config.keys():
			print("Error - required value " + requiredConfigParameter + " not set in config.json.")
			sys.exit(1)
	return config
