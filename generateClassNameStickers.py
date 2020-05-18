#!/usr/bin/python

# A script to produce name labels for each pupil, on a per-class basis. Uses reportLab to output printable PDF documents sized
# to fit Avery L7160 label sheets.

# Standard libraries.
import os
import sys

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

# Data-handling.
import pandas

# Our own library.
import dataLib

# Load the config file.
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
labelsRoot = config["dataFolder"] + os.sep + "Labels"
formLabelsRoot = labelsRoot + os.sep + "Form Labels"
spineLabelsRoot = labelsRoot + os.sep + "Spine Labels"
os.makedirs(formLabelsRoot, exist_ok=True)
os.makedirs(spineLabelsRoot, exist_ok=True)

# We are printing on Avery L7160 labels (A4, 7 rows of 3 labels) - set the page size and borders, in mm.
pageWidth = 210
pageHeight = 297
labelsX = 3
labelsY = 7
labelWidth = 63.5
labelHeight = 38.1
labelBorder = 40
labelHorizontalGap = 3
lineSpacing = 30
initialFontSize = 132
fontSizeStep = 4
leftBorder = (pageWidth - ((labelWidth * labelsX) + (labelHorizontalGap * 2))) / 2
topBorder = (pageHeight - (labelHeight * labelsY)) / 2

# Splits a string into two as-even-as-possible strings, split by space.
def evenlySplitString(theString):
	theString = theString.strip()
	if theString.find(" ") == -1:
		return(theString, "")
	stringSplit = theString.split(" ")
	if len(stringSplit) == 2:
		return(stringSplit[0], stringSplit[1])
	result1 = ""
	result2 = ""
	lowestDiff = 999
	for pl in range(1, len(stringSplit)):
		tempResult1 = " ".join(stringSplit[:pl])
		tempResult2 = " ".join(stringSplit[pl:])
		tempDiff = abs(len(tempResult1)-len(tempResult2))
		if tempDiff < lowestDiff:
			result1 = tempResult1
			result2 = tempResult2
			lowestDiff = tempDiff
	return(result1, result2)

# Set up a bunch of different font sizes for use with name labels.
fonts = {}
for fontSize in range(4, 129, 4):
	fonts[fontSize] = PIL.ImageFont.truetype("DejaVuSerif.ttf", fontSize)

print("Writing per-form PDF Stickers...")
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

forms = {}
for pupilsIndex, pupilsValue in pupils.iterrows():
	forms[pupilsValue["Form"]] = 1

for form in forms.keys():
	# Create the blank PDF document to start drawing page elements on.
	pdfCanvas = reportlab.pdfgen.canvas.Canvas(formLabelsRoot + os.sep + form + ".pdf")
	labelCount = 0
	for pupilsIndex, pupilsValue in pupils.iterrows():
		if form == pupilsValue["Form"]:
			labelX = labelCount % labelsX
			labelY = ((labelCount - labelX) / labelsX) % labelsY
			
			# Create a blank image to place the label details on.
			labelImageWidth = int(labelWidth*10)
			labelImageHeight = int(labelHeight*10)
			labelImage = PIL.Image.new("RGB", (labelImageWidth,labelImageHeight), (255, 255, 255))
			
			# Draw the pupil's full name on the label image, centred, 20 pixels down from the top.
			fontSize = initialFontSize
			line1Width = labelImageWidth
			line1Height = labelImageHeight
			line2Width = labelImageWidth
			line2Height = labelImageHeight
			textDrawer = PIL.ImageDraw.Draw(labelImage)
			line1Text, line2Text = evenlySplitString(pupilsValue["GivenName"] + " " + pupilsValue["FamilyName"])
			while line1Width >= (labelImageWidth-labelBorder) or line2Width >= (labelImageWidth-labelBorder) or (line1Height + lineSpacing + line2Height) >= labelImageHeight:
				fontSize = fontSize - fontSizeStep
				line1Width, line1Height = textDrawer.textsize(line1Text, font=fonts[fontSize])
				line2Width, line2Height = textDrawer.textsize(line2Text, font=fonts[fontSize])
			textDrawer.text((int((labelImageWidth-line1Width)/2), (labelBorder / 2)), line1Text, fill="black", font=fonts[fontSize])
			textDrawer.text((int((labelImageWidth-line2Width)/2), line1Height+lineSpacing), line2Text, fill="black", font=fonts[fontSize])
            
			# Place the label image on the PDF document.
			pdfCanvas.drawInlineImage(labelImage, (leftBorder+(labelX*(labelWidth+labelHorizontalGap)))*reportlab.lib.units.mm, (pageHeight-(topBorder+((labelY+1)*labelHeight)))*reportlab.lib.units.mm, labelWidth*reportlab.lib.units.mm, labelHeight*reportlab.lib.units.mm)
			
			labelCount = labelCount + 1
	# Save the PDF document.
	pdfCanvas.save()
	
for form in forms.keys():
	# Create the blank PDF document to start drawing page elements on.
	pdfCanvas = reportlab.pdfgen.canvas.Canvas(spineLabelsRoot + os.sep + form + ".pdf")
	labelCount = 0
	for pupilsIndex, pupilsValue in pupils.iterrows():
		if form == pupilsValue["Form"]:
			labelX = labelCount % labelsX
			labelY = ((labelCount - labelX) / labelsX) % labelsY
			
			# Create a blank image to place the label details on.
			labelImageWidth = int(labelWidth*10)
			labelImageHeight = int((labelHeight/3)*10)
			labelImage = PIL.Image.new("RGB", (labelImageWidth,labelImageHeight), (255, 255, 255))
			
			# Draw the pupil's given name.
			fontSize = initialFontSize
			lineWidth = labelImageWidth
			lineHeight = labelImageHeight / 3
			textDrawer = PIL.ImageDraw.Draw(labelImage)
			while lineWidth >= (labelImageWidth-labelBorder) or lineHeight >= labelImageHeight:
				fontSize = fontSize - fontSizeStep
				lineWidth, lineHeight = textDrawer.textsize(pupilsValue["GivenName"], font=fonts[fontSize])
			textDrawer.text((int((labelImageWidth-lineWidth)/2), (labelBorder / 2)), lineText, fill="black", font=fonts[fontSize])
            
			# Place the label image on the PDF document.
			pdfCanvas.drawInlineImage(labelImage, (leftBorder+(labelX*(labelWidth+labelHorizontalGap)))*reportlab.lib.units.mm, (pageHeight-(topBorder+((labelY+1)*labelHeight)))*reportlab.lib.units.mm, labelWidth*reportlab.lib.units.mm, labelHeight*reportlab.lib.units.mm)
			
			labelCount = labelCount + 1
	# Save the PDF document.
	pdfCanvas.save()
