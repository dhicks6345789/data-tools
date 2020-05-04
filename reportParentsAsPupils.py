#!/usr/bin/python
import os
import sys
import json
import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Make sure the output folder exists.
reportsRoot = config["dataFolder"] + os.sep + "Reports"
outputRoot = reportsRoot + os.sep + "Parents Joined To Classrooms As Pupils"
os.makedirs(outputRoot, exist_ok=True)

# Input data headings:
# Parents:
# Output in CSV format:
parentsAsPupils = pandas.DataFrame(columns=["First Name","Last Name","Email","Classroom","Classroom Teachers"])

parents = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)

#for parentsIndex, parentsValues in parents.iterrows():
#	parentsValues["email"]

parentsAsPupils.to_csv(outputRoot + os.sep + "report.csv", index=False)
