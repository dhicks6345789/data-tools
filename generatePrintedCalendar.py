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

# PyPDFs - used for merging existing PDF documents.
import PyPDF2



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

pdfsToMerge = []

# Check to see if there is content to merge.
frontMatterPath = calendarsFolder + os.sep + outputFilename + os.sep + "frontMatter.pdf"
if os.path.exists(frontMatterPath):
	print("Found front matter...")
	pdfsToMerge.append(frontMatterPath)

pdfsToMerge.append("temp.pdf")

backMatterPath = calendarsFolder + os.sep + outputFilename + os.sep + "backMatter.pdf"
if os.path.exists(backMatterPath):
	print("Found back matter...")
	pdfsToMerge.append(backMatterPath)

# Get ready to write out a formatted PDF document. We are printing on A5paper - set the page size and borders, in mm.
pageWidth = 148
pageHeight = 210
borderSize = 7
leftX = borderSize
rightX = pageWidth-borderSize
topY = pageHeight-borderSize
bottomY = borderSize
lineHeight = 8

# Create the blank PDF document and start drawing page elements.
pdfCanvas = reportlab.pdfgen.canvas.Canvas("temp.pdf")
pdfCanvas.setPageSize((pageWidth*reportlab.lib.units.mm, pageHeight*reportlab.lib.units.mm))

pdfCanvas.line(leftX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm, rightX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm)
pdfCanvas.line(rightX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm, rightX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm)
pdfCanvas.line(rightX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm, leftX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm)
pdfCanvas.line(leftX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm, leftX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm)

pdfCanvas.showPage()
pdfCanvas.line(leftX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm, rightX*reportlab.lib.units.mm, topY*reportlab.lib.units.mm)

# Save the PDF document.
pdfCanvas.save()

pdfMerger = PyPDF2.PdfFileMerger()
for pdfToMerge in pdfsToMerge:
	pdfMerger.append(pdfToMerge)
pdfMerger.write(calendarsFolder + os.sep + outputFilename + ".pdf")

os.remove("temp.pdf")
