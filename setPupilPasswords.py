#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import random
import installLib

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

requiredConfigParameters = ["dataFolder"]

# Load the configuration file.
config = json.loads(installLib.readFile("config/config.json"))
for requiredConfigParameter in requiredConfigParameters:
	if not requiredConfigParameter in config.keys():
		print("Error - required value " + requiredConfigParameter + " not set in config.json.")
		sys.exit(1)

# Words used to generate passwords.
adjectives = ["Large","Small","Long","Short","Narrow","Deep","Flat","Whole","Low","High","Near","Far","Gone","Moving","Fast","Quick","Early","Late","Bright","Dark","Cloudy","Hot","Warm","Cool","Cold","Windy","Noisy","Loud","Quiet","Dry","Wet","Clear","Hard","Soft","Heavy","Light","Strong","Weak","Clean","Tidy","Dirty","Empty","Full","Thirsty","Hungry","Old","Fresh","Dead","Healthy","Sweet","Sour","Bitter","Salty","Good","Bad","Great","Useful","Cheap","Free","Strong","Weak","Able","Rich","Brave","Fine","Sad","Proud","Happy","Clever","Famous","Funny","Kind","Polite","Fair","Busy","Lazy","Lucky","Safe"]
nouns = ["Albatross","Antelope","Ant","Ape","Baboon","Badger","Bat","Bear","Beaver","Bee","Bird","Bittern","Boar","Buffalo","Caribou","Cat","Cow","Chicken","Coot","Crane","Crocodile","Crow","Deer","Dog","Dolphin","Dove","Duck","Eagle","Eel","Elephant","Elk","Falcon","Ferret","Fish","Fox","Frog","Goose","Giraffe","Gnat","Goat","Gorilla","Grouse","Hawk","Heron","Hornet","Horse","Hyena","Ibex","Jay","Jellyfish","Kangaroo","Kitten","Lark","Lion","Mackerel","Magpie","Mouse","Mole","Monkey","Moose","Owl","Oyster","Parrot","Penguin","Pheasant","Pig","Quail","Rabbit","Raccoon","Rat","Raven","Rook","Seagull","Seal","Sheep","Snake","Sparrow","Squirrel","Stork","Swan","Tiger","Toad","Trout","Turkey","Turtle","Vulture","Weasel","Whale","Wolf","Wombat","Wren","Zebra"]
# Returns a string containing a new password.
def generatePassword():
    return adjectives[random.randint(0, len(adjectives)-1)] + nouns[random.randint(0, len(nouns)-1)] + str(random.randint(10,99))

# Read the contens of a file.
def readFile(theFilename):
	inHandle = open(theFilename)
	inData = inHandle.read()
	inHandle.close()
	return inData

installLib.writeFile("fullEmailTemplate.html", readFile("config" + os.sep + "passwordReset" + os.sep + "emailTemplate.html") + "<br/>\n--<br/>\n<br/>\n" + readFile("config" + os.sep + "emailSignature" + os.sep + "emailSignature.html"))

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

def setPassword(theUser, thePassword):
	for pupilIndex, pupilEntry in pupils.iterrows():
		if pupilEntry["Username"] == theUser:
			# os.system("gam update user " + theUser + "@knightsbridgeschool.com password " + thePassword)
			print("Setting password for user " + theUser + "...")
			os.system("net user " + theUser + " " + thePassword + " /domain")
			#for emailAddress in str(pupilEntry["Contacts"]).split(" "):
				## Sending email from itsupport@knightsbridgeschool.com, replyto itsupport@knightsbridgeschool.com
				#os.system("gam sendemail " + emailAddress + " subject \"Knightsbridge School - Pupil Account Password Reset\" file fullEmailTemplate.html replace childName \"" + pupilEntry["GivenName"] + " " + pupilEntry["FamilyName"] + "\" replace childUsername " + pupilEntry["OldUsername"] + " replace childPassword " + thePassword + " replace name \"David Hicks\" replace title \"IT Helpdesk\" replace email ithelpdesk@knightsbridgeschool.com replace telephone \"020 7590 9004\" html 2>&1")

# Read the Forms and Yeargroups into one list.
classGroups = []
for yeargroup in readFile(config["dataFolder"] + os.sep + "yeargroups.csv").split("\n"):
	if not yeargroup == "" and not yeargroup in classGroups:
		classGroups.append(yeargroup)
for form in readFile(config["dataFolder"] + os.sep + "forms.csv").split("\n"):
	if not form == "" and not form in classGroups:
		classGroups.append(form)
		
os.makedirs(config["dataFolder"] + os.sep + "DefaultPupilPasswords", exist_ok=True)
if not os.path.exists(config["dataFolder"] + os.sep + "DefaultPupilPasswords" + os.sep + "defaultPasswords.csv"):
	installLib.writeFile(config["dataFolder"] + os.sep + "DefaultPupilPasswords" + os.sep + "defaultPasswords.csv", "ID,Name,Username,OldUsername,Form,DefaultPassword")

# Read the existing pupil default passwords.
defaultPasswords = pandas.read_csv(config["dataFolder"] + os.sep + "DefaultPupilPasswords" + os.sep + "defaultPasswords.csv", header=0)

#for passwordIndex, passwordEntry in defaultPasswords.iterrows():
#	pupilFound = False
#	for pupilIndex, pupil in pupils.iterrows():
#		if passwordEntry["Username"] == pupil["Username"]:
#			pupilFound = True
#	if not pupilFound:
#		print("Remove: " + passwordEntry["Username"])
	
for pupilIndex, pupil in pupils.iterrows():
	pupilFound = False
	for passwordIndex, passwordEntry in defaultPasswords.iterrows():
		if pupil["ID"] == passwordEntry["ID"]:
			pupilFound = True
			defaultPasswords.at[passwordIndex, "Name"] = pupil["GivenName"] + " " + pupil["FamilyName"]
			defaultPasswords.at[passwordIndex, "Username"] = pupil["Username"]
			defaultPasswords.at[passwordIndex, "OldUsername"] = pupil["OldUsername"]
			defaultPasswords.at[passwordIndex, "Form"] = pupil["Form"]

	if not pupilFound:
		defaultPasswords = defaultPasswords.append({"ID":pupil["ID"],"DefaultPassword":generatePassword()} , ignore_index=True)

if len(sys.argv) >= 3:
	if len(sys.argv) == 3 and sys.argv[1] == "-user":
		username = sys.argv[2]
		for passwordIndex, passwordEntry in defaultPasswords.iterrows():
			if passwordEntry["OldUsername"] == username:
				setPassword(username, passwordEntry["DefaultPassword"])
	elif len(sys.argv) == 3 and sys.argv[1] == "-group":
		groupname = sys.argv[2]
		for passwordIndex, passwordEntry in defaultPasswords.iterrows():
			if groupname in passwordEntry["Form"]:
				setPassword(passwordEntry["Username"], passwordEntry["DefaultPassword"])
		
installLib.writeFile(config["dataFolder"] + os.sep + "DefaultPupilPasswords" + os.sep + "defaultPasswords.csv", defaultPasswords.to_csv(index=False))
os.remove("fullEmailTemplate.html")

if len(sys.argv) >= 3:
	sys.exit(0)

# Get ready to write out a formatted PDF document per year / form group listing usernames and passwords.
# We are printing on A4 paper - set the page size and borders, in mm.
pageWidth = 210
pageHeight = 297
lineHeight = 8
leftBorder = 10
topBorder = 10

# A mid-gray background to make following lines on the page a bit easier.
lineImage = PIL.Image.new("RGB", (pageWidth-(leftBorder*2), lineHeight), (200, 200, 200))

for group in readFile(config["dataFolder"] + os.sep + "yeargroups.csv").split("\n") + readFile(config["dataFolder"] + os.sep + "forms.csv").split("\n"):
	if not group == "":
	#if group == "S4" or group == "S5":
		# Create the blank PDF document to start drawing page elements on.
		pdfCanvas = reportlab.pdfgen.canvas.Canvas(config["dataFolder"] + os.sep + "DefaultPupilPasswords" + os.sep + group + ".pdf")
		# Draw the form name and column headers.
		pdfCanvas.drawString(leftBorder*reportlab.lib.units.mm, (pageHeight-topBorder)*reportlab.lib.units.mm, "Group: " + group)
		pdfCanvas.drawString(leftBorder*reportlab.lib.units.mm, ((pageHeight-lineHeight)-topBorder)*reportlab.lib.units.mm, "Name")
		pdfCanvas.drawString((leftBorder+110)*reportlab.lib.units.mm, ((pageHeight-lineHeight)-topBorder)*reportlab.lib.units.mm, "Username")
		pdfCanvas.drawString((leftBorder+150)*reportlab.lib.units.mm, ((pageHeight-lineHeight)-topBorder)*reportlab.lib.units.mm, "Default Password")
		
		pupilCount = 2
		pageCount = 0
		for pupilIndex, pupil in pupils.iterrows():
			for passwordIndex, passwordEntry in defaultPasswords.iterrows():
				if pupil["ID"] == passwordEntry["ID"]:
					if group in pupil["Form"]:
						passwordEntry["FullName"] = pupil["GivenName"] + " " + pupil["FamilyName"]
						if pupilCount % 2 == 0:
							pdfCanvas.drawInlineImage(lineImage, leftBorder*reportlab.lib.units.mm, ((pageHeight-(lineHeight*(pupilCount-(pageCount*36))))-(topBorder+lineHeight/4))*reportlab.lib.units.mm, (pageWidth-(leftBorder*2))*reportlab.lib.units.mm, lineHeight*reportlab.lib.units.mm)
						#for (columnName, xPos) in [["FullName", 0],["OldUsername", 110],["DefaultPassword", 150]]:
						for (columnName, xPos) in [["FullName", 0],["Username", 110],["DefaultPassword", 150]]:
							pdfCanvas.drawString((leftBorder+xPos)*reportlab.lib.units.mm, ((pageHeight-(lineHeight*(pupilCount-(pageCount*36))))-topBorder)*reportlab.lib.units.mm, passwordEntry[columnName])
						pupilCount = pupilCount + 1
						if pupilCount == 36:
							pdfCanvas.showPage()
							pageCount = pageCount + 1
		# Save the PDF document.
		pdfCanvas.save()
