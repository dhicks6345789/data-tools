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

# Check the command line paramaters.
if not len(sys.argv) == 3:
	print("Usage: generatedPrintedCalendar URL outputFilename")
inputCalendar = sys.argv[1]
outputFilename = sys.argv[2]

# Make sure the input / output folder exists.
calendarsFolder = config["dataFolder"] + os.sep + "Calendars"
os.makedirs(calendarsFolder, exist_ok=True)

# Check to see if there is content to merge.
frontMatterPath = calendarsFolder + os.sep + outputFilename + os.sep + "frontMatter.docx"
if os.path.exists(frontMatterPath):
	print("Found front matter...")

backMatterPath = calendarsFolder + os.sep + outputFilename + os.sep + "backMatter.docx"
if os.path.exists(backMatterPath):
	print("Found back matter...")

# Get ready to write out a formatted PDF document. We are printing on A5paper - set the page size and borders, in mm.
pageWidth = 148
pageHeight = 210
borderSize = 7
leftX = borderSize
rightX = pageWidth-borderSize
topY = pageHeight-borderSize
bottomY = borderSize
lineHeight = 8

# Create the blank PDF document to start drawing page elements on.
pdfCanvas = reportlab.pdfgen.canvas.Canvas(calendarsFolder + os.sep + outputFilename + ".pdf")
pdfCanvas.setPageSize(pageWidth, pageHeight)
pdfCanvas.line(leftX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm, rightX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm)

# Save the PDF document.
pdfCanvas.save()
