#This program finds and deletes duplicates of files in a given directory
import os, hashlib, sys

__author__ = "OSA413"
__license__ = "MIT License"
__source__ = "https://github.com/OSA413/Garbage"

def delete_this(path="$cwd", make_sorted=False):
    if path == "$cwd":
        path = os.getcwd()

    file_list = [x for x in os.listdir(path) if os.path.isfile(x)]
    if make_sorted: file_list.sort()

    files = []

    for i in range(len(file_list)):
        if (i % (len(file_list) // 10) == 0): print(i // (len(file_list) // 10))
        with open(file_list[i], "rb") as f:
            sha = hashlib.sha256(f.read()).hexdigest()
            if sha in files:
                os.remove(file_list[i])
            else:
                files.append(sha)
                
if __name__ == "__main__":
    path = "$cwd"
    make_sorted = False
    
    if len(sys.argv) > 0:
        path = sys.argv[0]
    if len(sys.argv) > 1:
        make_sorted = True
        
    delete_this(path, make_sorted)
