"""
NOTE: make a back-up of the files before using.
This program finds and deletes duplicates of files in the current directory
Usage: place this file and run it. There will be only unique files at the end.
It checks only files that are in the same folder as this script (no subfolders).
"""
import os

files = list(filter(lambda fl: os.path.isfile(fl), os.listdir(os.getcwd())))
files_content = []

for i in range(len(files)):
    with open(files[i],"rb") as f:
        files_content.append(f.read())

dif = 0
for i in range(len(files)):
    if files_content.count(files_content[i-dif]) > 1:
        os.remove(files[i-dif])
        del files[i-dif]
        del files_content[i-dif]
        dif += 1
