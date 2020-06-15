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

yeargroups = pandas.read_csv(config["dataFolder"] + os.sep + "yeargroups.csv", header=None)
for yeargroupsIndex, yeargroupsValues in yeargroups.iterrows():
	if os.path.exists(yeargroupsValues[0] + " - " + currentTerm + ".xlsx"):
		print(yeargroupsValues[0])
