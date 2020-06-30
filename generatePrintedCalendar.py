#!/usr/bin/python
import os
import io
import sys
import json
import time
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
import reportlab.rl_config
import reportlab.pdfbase.pdfmetrics
import reportlab.pdfbase.ttfonts

# PyPDFs - used for merging existing PDF documents.
import PyPDF2

# Set the various measurements (in mm) we need to write out a formatted PDF document (A5 paper size).
pageWidth = 148
pageHeight = 210
borderSize = 7

leftX = borderSize
rightX = pageWidth-borderSize
topY = pageHeight-borderSize
bottomY = borderSize

lineHeight = 8
linePadding = 3
tableWidth = pageWidth-(borderSize*2)



def drawRightJustifiedString(thePDFCanvas, theString, rightXPos, theYPos):
	theStringWidth = thePDFCanvas.stringWidth(theString, "calendarFont", 12) / reportlab.lib.units.mm
	thePDFCanvas.drawString((rightXPos-theStringWidth)*reportlab.lib.units.mm, theYPos*reportlab.lib.units.mm, theString)

def drawCalendarPage(thePDFCanvas, headings):
	cellHeight = (pageHeight - ((borderSize*2) + lineHeight)) / (len(headings)-1)
	# A mid-gray background to make following lines on the page a bit easier.
	headingImage = PIL.Image.new("RGB", (tableWidth, lineHeight), (200, 200, 200))
	headingY = topY - lineHeight
	thePDFCanvas.drawString(leftX*reportlab.lib.units.mm, (headingY+linePadding)*reportlab.lib.units.mm, headings[0][0])
	drawRightJustifiedString(pdfCanvas, headings[0][1], rightX, headingY+linePadding)
	for heading in headings[1:]:
		pdfCanvas.drawInlineImage(headingImage, leftX*reportlab.lib.units.mm, (headingY-lineHeight)*reportlab.lib.units.mm, tableWidth*reportlab.lib.units.mm, lineHeight*reportlab.lib.units.mm)
		thePDFCanvas.line(leftX*reportlab.lib.units.mm, headingY*reportlab.lib.units.mm, rightX*reportlab.lib.units.mm, headingY*reportlab.lib.units.mm)
		yPos = headingY-lineHeight
		thePDFCanvas.line(leftX*reportlab.lib.units.mm, yPos*reportlab.lib.units.mm, rightX*reportlab.lib.units.mm, yPos*reportlab.lib.units.mm)
		thePDFCanvas.drawString((leftX+linePadding)*reportlab.lib.units.mm, (yPos+linePadding)*reportlab.lib.units.mm, heading[0])
		drawRightJustifiedString(pdfCanvas, heading[1], rightX-linePadding, yPos+linePadding)
		headingY = headingY - cellHeight
	thePDFCanvas.line(rightX*reportlab.lib.units.mm, (topY-lineHeight)*reportlab.lib.units.mm, rightX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm)
	thePDFCanvas.line(rightX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm, leftX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm)
	thePDFCanvas.line(leftX*reportlab.lib.units.mm, bottomY*reportlab.lib.units.mm, leftX*reportlab.lib.units.mm, (topY-lineHeight)*reportlab.lib.units.mm)

	
	
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

reportlab.rl_config.warnOnMissingFontGlyphs = 0
for item in os.listdir(calendarsFolder + os.sep + outputFilename):
	if item.lower().endswith(".ttf"):
		reportlab.pdfbase.pdfmetrics.registerFont(reportlab.pdfbase.ttfonts.TTFont("calendarFont", calendarsFolder + os.sep + outputFilename + os.sep + item))

# Create the blank PDF document and start drawing page elements.
pdfCanvas = reportlab.pdfgen.canvas.Canvas("temp.pdf")
pdfCanvas.setPageSize((pageWidth*reportlab.lib.units.mm, pageHeight*reportlab.lib.units.mm))
pdfCanvas.setFont("calendarFont", 12)

drawCalendarPage(pdfCanvas, (("Week 1", "Goldfish Week"), ("Monday", "No Clubs This Week"), ("Tuesday", ""), ("Wednesday", ""), ("Thursday", "")))
pdfCanvas.showPage()
drawCalendarPage(pdfCanvas, (("", "20th - 26th April 2020"), ("Friday", ""), ("Saturday", ""), ("Sunday", ""), ("Notes", "")))

# Save the PDF document.
pdfCanvas.save()

pdfMerger = PyPDF2.PdfFileMerger()
for pdfToMerge in pdfsToMerge:
	pdfMerger.append(pdfToMerge)
pdfMerger.write(calendarsFolder + os.sep + outputFilename + ".pdf")
