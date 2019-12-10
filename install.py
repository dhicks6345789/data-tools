#!/usr/bin/python
import os
import shutil

# Obtain and include the installLib library.
os.system("git clone https://github.com/dhicks6345789/install-lib.git")
shutil.copyfile("install-lib/installLib.py", ".")

print("Hello, world!")
