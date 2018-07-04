"""
Checks if a file exists.
A file can be found by the full name or a part of the name.
If the file exists, prints it's full path.
"""
import os

def find(directory,key_name):
    a = list(os.walk(directory))
    #Tries to use relative path if absolute is not present
    if a == []:
        a = list(os.walk(os.path.join(os.path.dirname(__file__),directory)))
    files_list = []
    for i in a:
        for j in i[1]:
            b = os.path.join(i[0],j)
            if key_name in b:
                files_list.append(b)
        for j in i[2]:
            b = os.path.join(i[0],j)
            if key_name in b:
                files_list.append(b)
    return files_list

if __name__ == "__main__":
    print(find(input("[Starting directory]>>> "),input("[Key word]>>> ")))
