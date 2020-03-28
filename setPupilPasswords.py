#!/usr/bin/python
import os
import re
import sys
import csv
import json
import pandas
import random
import installLib

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

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

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
	installLib.writeFile(config["dataFolder"] + os.sep + "DefaultPupilPasswords" + os.sep + "defaultPasswords.csv", "ID,DefaultPassword")

# Read the existing pupil default passwords.
defaultPasswords = pandas.read_csv(config["dataFolder"] + os.sep + "DefaultPupilPasswords" + os.sep + "defaultPasswords.csv", header=0)

for pupilIndex, pupil in pupils.iterrows():
	pupilFound = False
	for passwordIndex, passwordEntry in defaultPasswords.iterrows():
		if pupil["ID"] == passwordEntry["ID"]:
			pupilFound = True
	if not pupilFound:
		print(pupil["OldUsername"])
		defaultPasswords.append([pupil["ID"],generatePassword()])

print(defaultPasswords)
