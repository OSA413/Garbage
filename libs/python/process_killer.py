"""
(Not so, actually) Universal process killer
Rewritten to be used as a module.
"""
import os
import sys

def kill_process(process_name):
    #Security fix
    process_name = process_name.split(" ")[0].split(";")[0]

    #For Windows
    if sys.platform == "win32":
        os.popen("taskkill /IM "+str(process_name)+".exe /F")
        #.bin is used in some programs (e.g. LibreOffice)
        os.popen("@echo off\ntaskkill /IM "+str(process_name)+".bin /F")
    #For Linux (tested on Ubuntu)
    elif "linux" in sys.platform:
        os.popen("killall -I "+str(process_name))

if __name__ == "__main__":
    while True:
        kill_process(input(">>> "))
