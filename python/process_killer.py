#Universal process killer
#Original Code By OSA413 in Python 3.5.1
#Version 1.0.2.2

__author__ = "OSA413"
__version__ = "1.0.2.2"
__license__ = "MIT License"

import sys
import os
import time

PYTHON_VERSION = sys.version        #checking Python version

if PYTHON_VERSION.startswith("2"):  #If using Python 2.7.x
    input = raw_input               #input() in Python 2 works a bit differently than in Python 3

print("\tUniversal process killer by OSA413")
print("\tVersion: "+str(__version__))

while True:
    print("\nEnter process or task name you want to kill.")
    user_input = input()
    #For an easy exit
    if user_input == r"\q":
        exit()
    #For Windows
    if sys.platform == "win32":
        os.popen("taskkill /IM "+str(user_input)+".exe /F")
        #.bin is used in some programs (e.g. LibreOffice)
        os.popen("@echo off\ntaskkill /IM "+str(user_input)+".bin /F")
    #For Linux (tested on Ubuntu)
    elif "linux" in sys.platform:
        os.popen("killall -I "+str(user_input))
    else:
        print("Your OS is not supported.")
        print("Press Enter to exit")
        input()
        exit()
    time.sleep(1)
