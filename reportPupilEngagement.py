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

def roundDatetime(theDate):
	return theDate.replace(hour=0, minute=0, second=0, microsecond=0)

def dateToWorkingDaysAgo(theDate):
	if theDate == "Never":
		return "Never"
	daysAgo = 0
	today = roundDatetime(datetime.datetime.now())
	currentDate = roundDatetime(datetime.datetime.strptime(theDate, "%Y-%m-%dT%H:%M:%S.%fZ"))
	while currentDate < today:
		if not currentDate.isoweekday() in [6, 7]:
			daysAgo = daysAgo + 1
		currentDate = currentDate + datetime.timedelta(days=1)
	return daysAgo

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

columnPos = {"Name":0,"Username":70,"Year":105,"Login":None,"Classroom":None,"Last Active(Working Days)":125,"Login/Class":None}
columnNames = columnPos.keys()
report = pandas.DataFrame(columns=columnNames)

yearGroups = {}
for pupilsIndex, pupilsValues in pupils.iterrows():
	yearGroups[dataLib.yearCohortToGroup(pupilsValues["YearGroup"])] = 1

reportIndex = 0
mostRecentDate = datetime.datetime(2000, 1, 1)
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
					if (not lastLogin == "Never") and lastLogin > mostRecentDate:
						mostRecentDate = lastLogin
					lastLoginDays = dateToWorkingDaysAgo(activityValues["accounts:last_login_time"])
					lastClassroom = parseDate(activityValues["classroom:last_interaction_time"])
					if (not lastClassroom == "Never") and lastClassroom > mostRecentDate:
						mostRecentDate = lastClassroom
					lastClassroomDays = dateToWorkingDaysAgo(activityValues["classroom:last_interaction_time"])
					if lastLogin == "Never":
						lastActive = lastClassroom
						lastActiveDays = lastClassroomDays
					elif lastClassroom == "Never":
						lastActive = lastLogin
						lastActiveDays = lastLoginDays
					elif lastClassroom > lastLogin:
						lastActive =  lastClassroom
						lastActiveDays = lastClassroomDays
					else:
						lastActive = lastLogin
						lastActiveDays = lastLoginDays
					if lastActive == "Never":
						report.at[indexToUse, "Last Active(Working Days)"] = "Never"
					else:
						report.at[indexToUse, "Last Active(Working Days)"] = lastActive.strftime("%d/%m/%Y") + "(" + str(lastActiveDays) + ")"
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
			pdfCanvas.drawString(leftBorder*reportlab.lib.units.mm, (pageHeight-topBorder)*reportlab.lib.units.mm, "Year: " + str(yearGroup) + ", Most recent date: " + roundDatetime(mostRecentDate).strftime("%d/%m/%Y"))
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
