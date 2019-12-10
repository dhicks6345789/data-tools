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

installLib.validValueOptions = ["-googleClientID", "-googleClientSecret"]
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
	if not os.path.exists(installLib.userHome + os.sep + ".config" + os.sep + "rclone" + os.sep + "rclone.conf"):
		rclone = pexpect.popen_spawn.PopenSpawn("C:/Program Files/rclone/rclone.exe config")		
		rclone.expect("n/s/q>")
		rclone.send("n\n")
		rclone.expect("name>")
		rclone.send("drive\\r")
		rclone.expect("Storage>")
		rclone.send("drive\\r")
		rclone.expect("client_id>")
		rclone.send(installLib.userOptions["-googleClientID"] + "\\r")
		rclone.expect("client_secret>")
		rclone.send(installLib.userOptions["-googleClientSecret"] + "\\r")
		rclone.expect("scope>")
		rclone.send("drive.readonly\\r")
		rclone.expect("root_folder_id>")
		rclone.send("\\r")
		rclone.expect("service_account_file>")
		rclone.send("\\r")
		rclone.expect("y/n>")
		rclone.send("n\\r")
		rclone.expect("y/n>")
		rclone.send("n\\r")
		
# Check for GAM - set it up.
