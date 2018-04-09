"""
(Not so, actually) Universal process killer
Rewritten to be used as a module.
"""
import os
import sys

def kill_process():
    #For Windows
    if sys.platform == "win32":
        os.popen("taskkill /IM "+str(user_input)+".exe /F")
        #.bin is used in some programs (e.g. LibreOffice)
        os.popen("@echo off\ntaskkill /IM "+str(user_input)+".bin /F")
    #For Linux (tested on Ubuntu)
    elif "linux" in sys.platform:
        os.popen("killall -I "+str(user_input))

if __name__ == "__main__":
    while True:
        kill_process(input(">>> "))
