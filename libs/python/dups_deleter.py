#This program finds and deletes duplicates of files in a given directory
import os, hashlib, sys, glob

__author__ = "OSA413"
__license__ = "MIT License"
__source__ = "https://github.com/OSA413/Garbage"

def delete_this(path="$cwd", make_sorted=False):
    if path == "$cwd":
        path = os.getcwd()

    file_list = [x for x in glob.glob(path + "/**/*", recursive = True) if os.path.isfile(x)]
    if make_sorted: file_list.sort()
    shas = set()
    print(len(file_list))
    
    for i in file_list:
        if os.path.isfile(i):
            with open(i, "rb") as f:
                sha = hashlib.sha256(f.read()).hexdigest()
                if sha in shas:
                    os.remove(i)
                else:
                    shas.add(sha)

    print(len(shas))
                
if __name__ == "__main__":
    args = sys.argv[:]
    path = "$cwd"
    make_sorted = False
    
    if "--sorted" in args[1:]:
        make_sorted = True
        args.remove("--sorted")
    
    if len(args) > 1:
        path = args[1]

    delete_this(path, make_sorted)
