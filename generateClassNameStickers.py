#!/usr/bin/python

# A script to parse pupil / staff data in CSV format suitible for importing into the Scout library system and produce printable PDF documents of sheets of
# stickers usable as pupil / staff borrower cards. Note that we are reading in CSV files produced from our own script, so we can be sure they are well-formed,
# so we're just resding them in with a simple .split(",") function.

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

# Barcode - used to generate images of barcodes in standard formats.
import barcode.codex
import barcode.writer

# Takes an array of strings, returns a single string with those strings separated by spaces.
def combineStrings(theStrings):
    result = ""
    for theString in theStrings:
        result = result + theString + " "
    return(result[:-1])

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
        tempResult1 = combineStrings(stringSplit[:pl])
        tempResult2 = combineStrings(stringSplit[pl:])
        tempDiff = abs(len(tempResult1)-len(tempResult2))
        if tempDiff < lowestDiff:
            result1 = tempResult1
            result2 = tempResult2
            lowestDiff = tempDiff
    return(result1, result2)

# Set up a bunch of different font sizes for use with name labels.
fonts = {}
for fontSize in range(4, 129, 4):
    fonts[fontSize] = PIL.ImageFont.truetype("/usr/share/fonts/truetype/ttf-dejavu/DejaVuSerif.ttf", fontSize)

print "Writing per-form Scout Borrower PDF Stickers..."
CSVRoot = "/root/CSVData/Scout/BorrowersByFormCSV"
for CSVFilename in os.listdir(CSVRoot):
    pupils = []
    form = CSVFilename[:-4]
    CSVHandle = open(CSVRoot + os.sep + CSVFilename)
    for CSVLine in CSVHandle.readlines():
        if not CSVLine.startswith("Alias,Name"):
            pupils.append(CSVLine.strip().split(","))
    CSVHandle.close()
    
    # Create the blank PDF document to start drawing page elements on.
    pdfCanvas = reportlab.pdfgen.canvas.Canvas("/root/CSVData/Scout/BorrowersByFormPDFStickers/" + form + ".pdf")
    
    # We are printing on Avery L7160 labels - work out the page size and borders, in mm.
    pageWidth = 210
    pageHeight = 297
    labelWidth = 63.5
    labelHeight = 38.1
    labelHorizontalGap = 3
    leftBorder = (pageWidth - ((labelWidth * 3) + (labelHorizontalGap * 2))) / 2
    topBorder = (pageHeight - (labelHeight * 7)) / 2
    
    # Loop through each pupil.
    pageNumber = 1
    for pupilIndex in range(0,len(pupils)):
        # We loop by index number because we use that index to position the label on the page.
        labelX = pupilIndex % 3
        labelY = ((pupilIndex - labelX) / 3) % 7

        # Create a blank image to place the label details on.
        labelImageWidth = int(labelWidth*10)
        labelImageHeight = int(labelHeight*10)
        labelImage = PIL.Image.new("RGB", (labelImageWidth,labelImageHeight), (255, 255, 255))

        # Generate the barcode containing the pupil's Alias.
        barcodeObject = barcode.codex.Code39(pupils[pupilIndex][0], writer=barcode.writer.ImageWriter(), add_checksum=False)
        barcodeFilename = barcodeObject.save("barcode", {"text_distance":1.0, "font_size":20})
        barcodeImage = PIL.Image.open(barcodeFilename)
        barcodeImageWidth, barcodeImageHeight = barcodeImage.size
        barcodeImage = barcodeImage.crop((20, barcodeImageHeight/2, barcodeImageWidth-20, barcodeImageHeight-20))
        barcodeImageWidth, barcodeImageHeight = barcodeImage.size
        barcodeImage = barcodeImage.resize([int(barcodeImageWidth*1.5),int(barcodeImageHeight*1.5)],PIL.Image.ANTIALIAS)
        barcodeImageWidth, barcodeImageHeight = barcodeImage.size
        # Place the barcode in the centre at the bottom, 20 pixels from the bottom.
        labelImage.paste(barcodeImage,(int(((labelWidth*10)-barcodeImageWidth)/2), (int(labelHeight)*10)-(barcodeImageHeight+20)))
        
        # Draw the pupil's full name on the label image, centred, 20 pixels down from the top.
        fontSize = 132
        line1Width = labelImageWidth
        line1Height = labelImageHeight
        line2Width = labelImageWidth
        line2Height = labelImageHeight
        textDrawer = PIL.ImageDraw.Draw(labelImage)
        line1Text, line2Text = evenlySplitString(pupils[pupilIndex][1])
        while line1Width >= (labelImageWidth-40) or line2Width >= (labelImageWidth-40) or (line1Height + 30 + line2Height) >= (labelImageHeight-(barcodeImageHeight+40)):
            fontSize = fontSize - 4
            line1Width, line1Height = textDrawer.textsize(line1Text, font=fonts[fontSize])
            line2Width, line2Height = textDrawer.textsize(line2Text, font=fonts[fontSize])
        textDrawer.text((int((labelImageWidth-line1Width)/2), 20), line1Text, fill="black", font=fonts[fontSize])
        textDrawer.text((int((labelImageWidth-line2Width)/2), line1Height+30), line2Text, fill="black", font=fonts[fontSize])
            
        # Place the label image on the PDF document.
        pdfCanvas.drawInlineImage(labelImage, (leftBorder+(labelX*(labelWidth+labelHorizontalGap)))*reportlab.lib.units.mm, (pageHeight-(topBorder+((labelY+1)*labelHeight)))*reportlab.lib.units.mm, labelWidth*reportlab.lib.units.mm, labelHeight*reportlab.lib.units.mm)
        os.remove(barcodeFilename)
        
        # Do we need to start a new page?
        if pupilIndex < (len(pupils)-1):
            if (pupilIndex+1) % 21 == 0:
                pdfCanvas.showPage()
    
    # Save the PDF document.
    pdfCanvas.save()
    
print "Writing per-form Scout Borrower List PDF Lists..."
CSVRoot = "/root/CSVData/Scout/BorrowersByFormCSV"
for CSVFilename in os.listdir(CSVRoot):
    pupils = []
    form = CSVFilename[:-4]
    CSVHandle = open(CSVRoot + os.sep + CSVFilename)
    for CSVLine in CSVHandle.readlines():
        if not CSVLine.startswith("Alias,Name"):
            pupils.append(CSVLine.strip().split(","))
    CSVHandle.close()
    
    # Create the blank PDF document to start drawing page elements on.
    pdfCanvas = reportlab.pdfgen.canvas.Canvas("/root/CSVData/Scout/BorrowersByFormPDFList/" + form + ".pdf")
    
    # We are printing on A4 - work out the page size and borders, in mm.
    pageWidth = 210
    pageHeight = 297
    leftBorder = 20
    topBorder = 20
    numberOfRows = 10
    lineImageWidthMM = pageWidth-(leftBorder*2)
    lineImageHeightMM = (pageHeight-(topBorder*2)) / numberOfRows
    lineImageWidthPixels = int(lineImageWidthMM*10)
    lineImageHeightPixels = int(lineImageHeightMM*10)
    
    # Loop through each pupil.
    pageNumber = 1
    for pupilIndex in range(0,len(pupils)+1):
        # We loop by index number because we use that index to position the line on the page.
        lineY = pupilIndex % numberOfRows

        # Create a blank image to place the details on.
        lineColour = 255 - ((lineY % 2) * 100)
        lineImage = PIL.Image.new("RGB", (lineImageWidthPixels,lineImageHeightPixels), (lineColour, lineColour, lineColour))

        if pupilIndex == 0:
            barcodeImageWidth = 0
        else:
            # Generate the barcode containing the pupil's Alias.
            barcodeObject = barcode.codex.Code39(pupils[pupilIndex-1][0], writer=barcode.writer.ImageWriter(), add_checksum=False)
            barcodeFilename = barcodeObject.save("barcode", {"text_distance":1.0, "font_size":20})
            barcodeImage = PIL.Image.open(barcodeFilename)
            barcodeImageWidth, barcodeImageHeight = barcodeImage.size
            barcodeImage = barcodeImage.crop((20, barcodeImageHeight/2, barcodeImageWidth-20, barcodeImageHeight-20))
            barcodeImageWidth, barcodeImageHeight = barcodeImage.size
            barcodeImage = barcodeImage.resize([int(barcodeImageWidth*1.5),int(barcodeImageHeight*1.5)],PIL.Image.ANTIALIAS)
            barcodeImageWidth, barcodeImageHeight = barcodeImage.size
            # Place the barcode in the centre of the line image, right-aligned.
            lineImage.paste(barcodeImage, (lineImageWidthPixels-barcodeImageWidth, int((lineImageHeightPixels-barcodeImageHeight)/2)))
        
        # Draw the pupil's full name on the label image, left-aligned, vertically centred.
        fontSize = 132
        lineWidth = lineImageWidthPixels-barcodeImageWidth
        textDrawer = PIL.ImageDraw.Draw(lineImage)
        if pupilIndex == 0:
            lineText = "Form: " + form
        else:
            lineText = pupils[pupilIndex-1][1]
        while lineWidth >= (lineImageWidthPixels-barcodeImageWidth):
            fontSize = fontSize - 4
            lineWidth, lineHeight = textDrawer.textsize(lineText, font=fonts[fontSize])
        if pupilIndex == 0:
            xPos = int((lineImageWidthPixels-lineWidth)/2)
        else:
            xPos = 0
        textDrawer.text((xPos, int((lineImageHeightPixels-lineHeight)/2)), lineText, fill="black", font=fonts[fontSize])

        # Place the label image on the PDF document.
        pdfCanvas.drawInlineImage(lineImage, leftBorder*reportlab.lib.units.mm, (pageHeight-(((lineY+1)*lineImageHeightMM)+topBorder))*reportlab.lib.units.mm, lineImageWidthMM*reportlab.lib.units.mm, lineImageHeightMM*reportlab.lib.units.mm)
        if not pupilIndex == 0:
            os.remove(barcodeFilename)
        
        # Do we need to start a new page?
        if lineY == numberOfRows-1:
            pdfCanvas.showPage()
    
    # Save the PDF document.
    pdfCanvas.save()
