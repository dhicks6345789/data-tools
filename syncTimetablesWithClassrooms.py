#!/usr/bin/python
import os
import io
import sys
import json
import shutil
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



# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

currentTerm = "Summer 2020"

# Make sure the output folder exists.
timetablesRoot = config["dataFolder"] + os.sep + "Timetables"
os.makedirs(timetablesRoot, exist_ok=True)

# Get a list of all pupils.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

# Get a list of all yeargroups.
yeargroups = pandas.read_csv(config["dataFolder"] + os.sep + "yeargroups.csv", header=None)

# For each yeargroup...
for yeargroupsIndex, yeargroupsValues in yeargroups.iterrows():
	# ...see if there's a Timetable data file for each specific yeargroup...
	timetablePath = timetablesRoot + os.sep + yeargroupsValues[0] + " - " + currentTerm + ".xlsx"
	if os.path.exists(timetablePath):
		# ...and if so, determine which pupils are in that yeargroup.
		pupilGroup = []
		for pupilsIndex, pupilsValues in pupils.iterrows():
			if yeargroupsValues[0] in pupilsValues["Form"]:
				pupilGroup.append(pupilsValues)
		print(yeargroupsValues[0])
		for pupil in pupilGroup:
			print(pupil["OldUsername"])
		# Read the Timetable data file.
		print(timetablePath)
