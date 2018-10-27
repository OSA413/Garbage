"""
NOTE: make a back-up of the files before using.
This program finds and deletes duplicates of files in the current directory
Usage: place this file and run it. There will be only unique files at the end.
It checks only files that are in the same folder as this script (no subfolders).
"""
import os, hashlib

file_list = [x for x in os.listdir(os.getcwd()) if os.path.isfile(x)]
files = [[],[]]

for i in range(len(file_list)):
    with open(file_list[i], "rb") as f:
        files[0].append(file_list[i])
        files[1].append(hashlib.sha256(f.read()).hexdigest())

while files[0]:
    tmp_hash = files[1][0]
    del files[0][0]
    del files[1][0]
    
    for i in range(files[1].count(tmp_hash)):
        ind = files[1].index(tmp_hash)
        
        os.remove(files[0][ind])
        del files[0][ind]
        del files[1][ind]
