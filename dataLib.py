#!/usr/bin/python
import os
import json
import pandas

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
	return str(theString).strip()

# Rewrites a file wirth the given data, but only if that data has changed, otherwise the file is left as is.
# Stops otherwise identical files having their timestamps changed.
def rewriteCachedData(theFilename, theData):
	currentData = ""
	if os.path.exists(theFilename):
		currentData = readFile(theFilename)
	if currentData == theData:
		return False
	writeFile(theFilename, theData)
	return True

def readOptionsFile(theFilename, theColumns):
	options = {}
	if not os.path.exists(theFilename):
		configDataframe = pandas.DataFrame(columns=theColumns)
	elif theFilename.lower().endswith(".xlsx"):
		configDataframe = pandas.read_excel(theFilename, header=0)
	if "Option" in configDataframe.columns and "Value" in configDataframe.columns:
		for configIndex, configValue in classrooms.iterrows():
			options[configValue["Option"]] = configValue["Value"]
	return(options, configDataframe.drop(columns=["Option","Value"], errors="ignore"))

def writeDataframeFile(theFilename, theDataframe):
	if theFilename.lower().endswith(".xlsx"):
		theDataframe.to_excel("temp.xlsx", index=False)
		tempHandle = open("temp.xlsx", "rb")
		tempData = tempHandle.read()
		tempHandle.close()
		
		filenameData = None
		if os.path.exists(theFilename):
			filenameHandle = open(theFilename, "rb")
			filenameData = filenameHandle.read()
			filenameHandle.close()

		if tempData == filenameData:
			os.remove("temp.xlsx")
		else:
			os.replace("temp.xlsx", theFilename)

def yearCohortToGroup(theCohort):
	cohort = str(theCohort)
	if cohort == "12":
		return "Year 8"
	elif cohort == "13":
		return "Year 7"
	elif cohort == "14":
		return "Year 6"
	elif cohort == "15":
		return "Year 5"
	elif cohort == "16":
		return "Year 4"
	elif cohort == "17":
		return "Year 3"
	elif cohort == "18":
		return "Year 2"
	elif cohort == "19":
		return "Year 1"
	elif cohort == "20":
		return "Reception"
	elif cohort == "21":
		return "Nursery"
	return cohort
