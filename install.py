#!/usr/bin/python
import os
import shutil

# Obtain and import the installLib library - should work on Windows and Linux / MacOS.
if os.path.exists("install-lib"):
	os.system("git -C install-lib pull https://github.com/dhicks6345789/install-lib.git")
else:
	os.system("git clone https://github.com/dhicks6345789/install-lib.git")
shutil.copyfile("install-lib/installLib.py", "./installLib.py")
import installLib

validValueOptions = ["-googleClientID"]

installLib.getUserOption("")

print("Hello, world!")
# Check for Expect.
# Get user options.
# Check for rclone - set it up.
# Check for GAM - set it up.
