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

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
yeargroups = pandas.read_csv(config["dataFolder"] + os.sep + "yeargroups.csv", header=None)
for yeargroupsIndex, yeargroupsValues in yeargroups.iterrows():
	if os.path.exists(timetablesRoot + os.sep + yeargroupsValues[0] + " - " + currentTerm + ".xlsx"):
		pupilGroup = []
		for pupilsIndex, pupilsValues in pupils.iterrows():
			if yeargroupsValues[0] in pupilsValues["Form"]:
				pupilGroup.append(pupilsValues)
		print(pupilGroup)
