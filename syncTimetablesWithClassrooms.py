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

# Make sure the output folder exists.
outputRoot = config["dataFolder"] + os.sep + "Timetables"
os.makedirs(outputRoot, exist_ok=True)

pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

print("More stuff goes here...")
