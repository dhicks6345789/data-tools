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

# A function to write a bunch of commands to a batch file and then run.
def runAsBatchFile(theBatchFileLines):
	outputHandle = open("temp.bat", "w")
	outputHandle.write("@echo off\n")
	for batchFileLine in theBatchFileLines:
		outputHandle.write(batchFileLine + "\n")
	outputHandle.close()
	os.system("temp.bat")
	os.remove("temp.bat")

installLib.validValueOptions = ["-googleClientID", "-googleClientSecret", "-configFolder", "-dataFolder"]
installLib.getUserOption("-googleClientID", "Enter the Google Client ID used to connect rclone")
installLib.getUserOption("-googleClientSecret", "Enter the Google Client Secret used to connect rclone")

installLib.getUserOption("-configFolder", "Enter the Google Drive folder that contains the Data Tools config")
installLib.getUserOption("-dataFolder", "Enter the (writeable) Google Drive folder that contains the MIS Data")

# Check if we're on Windows.
if os.name == "nt":
	# Make sure PExpect is installed.
	installLib.runIfPathMissing(installLib.pythonHome + os.sep + "Lib" + os.sep + "site-packages" + os.sep + "pexpect", "\"" + installLib.pipExe + "\" install pexpect")
	import pexpect
	import pexpect.popen_spawn
	
	# Code goes here - check for rclone, install it if needed.
	rclonePath = "C:\\Program Files\\rclone\\rclone.exe"
	
	# Make sure rclone is configured.
	if not os.path.exists(installLib.userHome + os.sep + ".config" + os.sep + "rclone" + os.sep + "rclone.conf"):
		rclone = pexpect.popen_spawn.PopenSpawn(rclonePath.replace("\\", "/") + " config")		
		rclone.expect("n/s/q>")
		rclone.send("n\n")
		rclone.expect("name>")
		rclone.send("drive\n")
		rclone.expect("Storage>")
		rclone.send("drive\n")
		rclone.expect("client_id>")
		rclone.send(installLib.userOptions["-googleClientID"] + "\n")
		rclone.expect("client_secret>")
		rclone.send(installLib.userOptions["-googleClientSecret"] + "\n")
		rclone.expect("scope>")
		rclone.send("drive\n")
		rclone.expect("root_folder_id>")
		rclone.send("\n")
		rclone.expect("service_account_file>")
		rclone.send("\n")
		rclone.expect("y/n>")
		rclone.send("n\n")
		rclone.expect("y/n>")
		rclone.send("y\n")
		rclone.expect("y/n>")
		rclone.send("n\n")
		rclone.expect("y/e/d>")
		rclone.send("y\n")
		rclone.expect("e/n/d/r/c/s/q>")
		rclone.send("q\n")

	# At this point, we should be able to get data from Google Drive.
	runAsBatchFile(["echo Getting data from Google Drive.",
		"\"" + rclonePath + "\" sync \"drive:" + installLib.userOptions["-configFolder"] + "\" config",
		"\"" + rclonePath + "\" sync \"drive:" + installLib.userOptions["-dataFolder"] + "\" \"..\\Documents\\User Tools Data\""])
	
	# Make sure XLRD (Python library for handling Excel files, required for Excel support in Pandas) is installed.
	installLib.runIfPathMissing("C:\\Program Files\\"+installLib.pythonVersion+"\\Lib\\site-packages\\xlrd", "py -m pip install xlrd")
	
	# Make sure OpenPyXL (Python library for handling Excel files, required for Excel support in Pandas) is installed.
	installLib.runIfPathMissing("C:\\Program Files\\"+installLib.pythonVersion+"\\Lib\\site-packages\\openpyxl", "py -m pip install openpyxl")

	# Make sure Pandas (Python data-analysis library) is installed.
	installLib.runIfPathMissing("C:\\Program Files\\"+installLib.pythonVersion+"\\Lib\\site-packages\\pandas", "py -m pip install pandas")

	# Make sure Numpy (Python maths library) is installed.
	installLib.runIfPathMissing("C:\\Program Files\\"+installLib.pythonVersion+"\\Lib\\site-packages\\numpy", "py -m pip install numpy")
	
	# Make sure ReportLab (Python PDF creation library) is installed.
	installLib.runIfPathMissing("C:\\Program Files\\"+installLib.pythonVersion+"\\Lib\\site-packages\\reportlab", "py -m pip install reportlab")
	
	# Make sure PyPDF2 (Python PDF manipulation library) is installed.
	installLib.runIfPathMissing("C:\\Program Files\\"+installLib.pythonVersion+"\\Lib\\site-packages\\PyPDF2", "py -m pip install PyPDF2")
	
# Code goes here - check for GAM, install it and set it up if needed.
