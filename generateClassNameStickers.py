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
	for pupilsIndex, pupilsValue in pupils.iterrows():
		if form == pupilsValue["Form"]:
			print(evenlySplitString(pupilsValue["GivenName"] + " " + pupilsValue["FamilyName"]))