#!/usr/bin/python
import os
import io
import sys
import json
import pandas
import dataLib
import datetime

# PIL - the Python Image Library, used for bitmap image manipulation.
import PIL
import PIL.ImageFont
import PIL.ImageDraw

# ReportLab - used for PDF document generation.
import reportlab.lib.units
import reportlab.lib.utils
import reportlab.lib.colors
import reportlab.pdfgen.canvas
import reportlab.lib.pagesizes
import reportlab.graphics.renderPM

def intToConstrainedPercentage(theValue, theMin, theMax):
	result = theValue
	if result < theMin:
		result = theMin
	if result > theMax:
		result = theMax
	return (result - theMin) / (theMax - theMin)

def dateToDaysAgo(theDate):
	if theDate == "Never":
		return "Never"
	return (datetime.datetime.now() - datetime.datetime.strptime(theDate, "%Y-%m-%dT%H:%M:%S.%fZ")).days

def parseDate(theDate):
	if theDate == "Never":
		return "Never"
	return datetime.datetime.strptime(theDate, "%Y-%m-%dT%H:%M:%S.%fZ")



# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
reportsRoot = config["dataFolder"] + os.sep + "Reports"
outputRoot = reportsRoot + os.sep + "Pupil Engagement"
os.makedirs(outputRoot, exist_ok=True)

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
activity = pandas.read_csv(config["dataFolder"] + os.sep + "Reports" + os.sep + "userActivity.csv", header=0)

columnPos = {"Name":0,"Username":70,"Year":100,"Login":None,"Classroom":None,"Last Active":115,"Login/Class":140,}
columnNames = columnPos.keys()
report = pandas.DataFrame(columns=columnNames)

yearGroups = {}
for pupilsIndex, pupilsValues in pupils.iterrows():
	yearGroups[dataLib.yearCohortToGroup(pupilsValues["YearGroup"])] = 1
reportIndex = 0
print("Processing data by year group...")
for yearGroup in yearGroups.keys():
	print("Processing " + yearGroup + "...")
	for pupilsIndex, pupilsValues in pupils.iterrows():
		if dataLib.yearCohortToGroup(pupilsValues["YearGroup"]) == yearGroup:
			for activityIndex, activityValues in activity.iterrows():
				username = ""
				if activityValues["email"] == pupilsValues["Username"] + "@knightsbridgeschool.com":
					username = pupilsValues["Username"]
					altUsername = pupilsValues["OldUsername"]
				elif activityValues["email"] == pupilsValues["OldUsername"] + "@knightsbridgeschool.com":
					username = pupilsValues["OldUsername"]
					altUsername = pupilsValues["Username"]
				if not username == "":
					indexToUse = reportIndex
					usernameList = report["Username"].tolist()
					if altUsername in usernameList:
						altUsernameIndex = usernameList.index(altUsername)
						if report.at[altUsernameIndex, "Login"] == "Never":
							indexToUse = altUsernameIndex
					else:
						reportIndex = reportIndex + 1
					report.at[indexToUse, "Name"] = pupilsValues["GivenName"] + " " + pupilsValues["FamilyName"]
					report.at[indexToUse, "Username"] = username
					report.at[indexToUse, "Year"] = dataLib.yearCohortToGroup(yearGroup)
					report.at[indexToUse, "Login"] = activityValues["accounts:last_login_time"]
					report.at[indexToUse, "Classroom"] = activityValues["classroom:last_interaction_time"]
					
					lastLogin = parseDate(activityValues["accounts:last_login_time"])
					lastClassroom = parseDate(activityValues["classroom:last_interaction_time"])
					if lastLogin == "Never":
						lastActive = lastClassroom
					elif lastClassroom == "Never":
						lastActive = lastLogin
					elif lastClassroom < lastLogin:
						lastActive =  lastClassroom
					else:
						lastActive = lastLogin
					report.at[indexToUse, "Last Active"] = lastActive.strftime("%d/%m/%Y")
					
					#lastLoginDays = dateToDaysAgo(activityValues["accounts:last_login_time"])
					#lastClassroomDays = dateToDaysAgo(activityValues["classroom:last_interaction_time"])
					#report.at[indexToUse, "Login/Class"] = (str(lastLoginDays) + "/" + str(lastClassroomDays)).replace("ever","")
					#if lastLoginDays == "Never":
					#	lastActivity = lastClassroomDays
					#elif lastClassroomDays == "Never":
					#	lastActivity = lastLoginDays
					#elif lastClassroomDays < lastLoginDays:
					#	lastActivity = lastClassroomDays
					#else:
					#	lastActivity = lastLoginDays
					#if lastActivity == "Never":
					#	report.at[indexToUse, "Activity, %"] = 0
					#else:
					#	report.at[indexToUse, "Activity, %"] = int(round(1 - intToConstrainedPercentage(lastActivity, 3, 8), 2) * 100)
					# pdfCanvas.setFillColorRGB(colourValue,1-colourValue,0)

# Write out the CSV report.
report.to_csv(outputRoot + os.sep + "report.csv", index=False)

# Get ready to write out a formatted PDF document per year group.
# We are printing on A4 paper - set the page size and borders, in mm.
pageWidth = 210
pageHeight = 297
lineHeight = 8
leftBorder = 10
topBorder = 10

# A mid-gray background to make following lines on the page a bit easier.
lineImage = PIL.Image.new("RGB", (pageWidth-(leftBorder*2), lineHeight), (200, 200, 200))

for yearGroup in yearGroups.keys():
	print("Generating report: " + yearGroup + ".pdf")
	lineNumber = 1
	pdfCanvas = reportlab.pdfgen.canvas.Canvas(outputRoot + os.sep + yearGroup + ".pdf")	
	for reportIndex, reportValues in report.iterrows():
		# Draw the report name and column headers.
		if lineNumber == 1:
			pdfCanvas.drawString(leftBorder*reportlab.lib.units.mm, (pageHeight-topBorder)*reportlab.lib.units.mm, "Year: " + str(yearGroup))
			for columnName in columnNames:
				if not columnPos[columnName] == None:
					pdfCanvas.drawString((leftBorder+columnPos[columnName])*reportlab.lib.units.mm, ((pageHeight-lineHeight)-topBorder)*reportlab.lib.units.mm, columnName)
			lineNumber = 2
		if reportValues["Year"] == yearGroup:
			for columnName in columnNames:
				if not columnPos[columnName] == None:
					if lineNumber % 2 == 0:
						pdfCanvas.drawInlineImage(lineImage, leftBorder*reportlab.lib.units.mm, ((pageHeight-(lineHeight*(lineNumber+1))-(int(lineHeight/4)))-topBorder)*reportlab.lib.units.mm, (pageWidth-(leftBorder*2))*reportlab.lib.units.mm, lineHeight*reportlab.lib.units.mm)
					pdfCanvas.setFillColorRGB(0,0,0)
					columnValue = str(reportValues[columnName])
					if columnName == "Year":
						columnValue = columnValue.replace("Reception","Rec").replace("Year ","")
					pdfCanvas.drawString((leftBorder+columnPos[columnName])*reportlab.lib.units.mm, ((pageHeight-(lineHeight*lineNumber))-topBorder)*reportlab.lib.units.mm, columnValue)
			lineNumber = lineNumber + 1
			if lineNumber == 36:
				pdfCanvas.showPage()
				lineNumber = 1
	# Save the PDF document.
	pdfCanvas.save()
