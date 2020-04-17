import os

def readFile(theFilename):
	inHandle = open(theFilename)
	result = inHandle.read()
	inHandle.close()
	return result

def runCommand(theCommand):
	commandHandle = os.popen(theCommand)
	result = commandHandle.readlines()
	commandHandle.close()
	return result

def removeBlanks(theString):
	result = ""
	for line in theString.split("\n"):
		line = line.strip()
		if not line == "":
			result = result + line + "\n"
	return result.strip()
