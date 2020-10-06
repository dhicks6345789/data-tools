#!/usr/bin/python
import os
#import re
#import io
#import sys
#import csv
#import json
#import pandas
import dataLib

# Load the config file (set by the system administrator).
config = dataLib.loadConfig(["dataFolder"])

# Read the existing basic pupils data.
pupils = pandas.read_csv(config["dataFolder"] + os.sep + "pupils.csv", header=0)
for pupilsIndex, pupilsValue in pupils.iterrows():
  print(pupilsValue["Username"])
