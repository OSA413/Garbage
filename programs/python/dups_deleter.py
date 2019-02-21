"""
NOTE: make a back-up of the files before using.
This program finds and deletes duplicates of files in the current directory
Usage: place this file and run it. There will be only unique files at the end.
It checks only files that are in the same folder as this script (no subfolders).
"""
import os, hashlib

file_list = [x for x in os.listdir(os.getcwd()) if os.path.isfile(x)]
files = []

for i in range(len(file_list)):
    if (i % (len(file_list) // 10) == 0): print(i // (len(file_list) // 10))
    with open(file_list[i], "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
        if sha in files:
            os.remove(file_list[i])
        else:
            files.append(sha)
