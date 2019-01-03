"""
Checks if a file exists.
A file can be found by the full name or a part of the name.
If the file exists, prints it's full path.
"""

__author__ = "OSA413"
__license__ = "MIT License"
__source__ = "https://github.com/OSA413/Garbage"

import os
import sys

def find(directory, key_name="", case_sensitive=True, recursive=False):
    files_list = []

    if not case_sensitive:
        key_name = key_name.lower()

    if recursive:
        a = list(os.walk(directory))
        #Tries to use relative path if absolute is not present
        if a == []:
            a = list(os.walk(os.path.join(os.path.dirname(__file__),directory)))
        if a == []:
            os.listdir(directory) #raising error if directory is not present

        for i in a:
            for j in i[1]:
                b = os.path.join(i[0],j)
                c = b
                if not case_sensitive:
                    c = b.lower()
                
                if key_name in c:
                    files_list.append(b)
            for j in i[2]:
                b = os.path.join(i[0],j)
                c = b
                if not case_sensitive:
                    c = b.lower()

                if key_name in c:
                    files_list.append(b)

    else:
        try:
            a = os.listdir(directory)
        except:
            a = os.listdir(os.path.join(os.path.dirname(__file__),directory))
        files_list = [os.path.join(*os.path.split(directory),x) for x in a if key_name in x]

    return files_list

if __name__ == "__main__":
    sys_argv = sys.argv[:]

    if "--help" in sys_argv[1:]:
        sys_argv = []

    recursive = False
    if "-r" in sys_argv[1:]:
        recursive = True
        del sys_argv[sys_argv.index("-r")]

    case_sensitive = True
    if "-i" in sys_argv[1:]:
        case_sensitive = False
        del sys_argv[sys_argv.index("-i")]

    if len(sys_argv) == 1:
        txt_len = 27
        sys_argv.append(input("[Starting directory]>>> ".rjust(txt_len)))
        sys_argv.append(input("[Key word]>>> ".rjust(txt_len)))
        case_sensitive  = input("Case-sensitively? [Y/N]>>> ".rjust(txt_len)).lower() == "y"
        recursive       = input("Recursively? [Y/N]>>> ".rjust(txt_len)).lower() == "y"

    if len(sys_argv) == 2:
        print("\n".join(find(sys_argv[1], case_sensitive=case_sensitive, recursive=recursive)))
    elif len(sys_argv) == 3:
        print("\n".join(find(sys_argv[1], sys_argv[2], case_sensitive=case_sensitive,recursive=recursive)))
    else:
        print("Usage: finder.py [starting directory] [key word=\"\"] [flags]")
        print("Prints found directories and files in [starting directory] that contain [key word]")
        print("")
        print("Flags:")
        txt_len0 = 8
        space = 4
        print("-r".rjust(txt_len0)+" "*space+       "Search recursively.")
        print("-i".rjust(txt_len0)+" "*space+       "Search case-insensitively.")
        print("--help".rjust(txt_len0)+" "*space+   "Show this message.")
