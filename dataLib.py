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

# Handy utility function to write a file. Takes a file path and either a single string or an array of strings. If an array, will write each
# string to the given file path with a newline at the end.
def writeFile(theFilename, theFileData):
	fileDataHandle = open(theFilename, "w")
	if isinstance(theFileData, str):
		fileDataHandle.write(theFileData)
	else:
		for dataLine in theFileData:
			fileDataHandle.write((str(dataLine) + "\n").encode())
	fileDataHandle.close()

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
def loadConfig(requiredConfigParameters):
	# Load the configuration file.
	config = json.loads(readFile("config/config.json"))
	for requiredConfigParameter in requiredConfigParameters:
		if not requiredConfigParameter in config.keys():
			print("Error - required value " + requiredConfigParameter + " not set in config.json.")
			sys.exit(1)
	return config

def floatToStr(theValue):
	if isinstance(theValue, float):
		if theValue == 0:
			return ""
	return str(theValue)

# A function to remove "nan" strings from data - /really/ shouldn't be needed...
def noNan(theString):
	if str(theString) == "nan" or str(theString) == "0":
		return ""
	return str(theString.strip())

# Rewrites a file wirth the given data, but only if that data has changed, otherwise the file is left as is.
# Stops otherwise identical files having their timestamps changed.
def rewriteCachedData(theFilename, theData):
	currentData = readFile(theFilename)
	if theData == "" or currentData == theData:
		return False
	writeFile(theFilename, theData)
	return True
