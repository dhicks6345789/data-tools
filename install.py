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

# Make sure PExpect is installed.
if os.name == "nt":
	installLib.runIfPathMissing(pythonHome + os.sep + "Lib" + os.sep + "site-packages" + os.sep + "pexpect", "\"" + pipExe + "\" install pexpect")
import pexpect



# Check for rclone - set it up.

#print("Configuring MariaDB...")
#    runExpect([
#        "spawn /usr/bin/mysql_secure_installation",
#        "expect \"(enter for none):\"",
#        "send \"\\r\"",
#        "expect \"\\[Y/n\\]\"",
#        "send \"n\\r\"",
#        "interact"
#    ])

# Check for GAM - set it up.
