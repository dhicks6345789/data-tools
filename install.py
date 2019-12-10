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

validValueOptions = ["-googleClientID", "-googleClientSecret"]
installLib.getUserOption("-googleClientID", "Enter the Google Client ID used to connect rclone")
installLib.getUserOption("-googleClientSecret", "Enter the Google Client Secret used to connect rclone")

# Chec if we're on Windows.
if os.name == "nt":
	# Make sure PExpect is installed.
	installLib.runIfPathMissing(installLib.pythonHome + os.sep + "Lib" + os.sep + "site-packages" + os.sep + "pexpect", "\"" + installLib.pipExe + "\" install pexpect")
	import pexpect
	import pexpect.popen_spawn
	
	# To do - Check for rclone.
	# Make sure rclone is configured.
	rclone = pexpect.popen_spawn.PopenSpawn("\"C:\Program Files\rclone\rclone.exe\" config")
	rclone.interact()

# Check for GAM - set it up.
