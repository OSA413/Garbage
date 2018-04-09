"""
Checks if a file exists.
A file can be found by the full name or a part of the name.
If the file exists, prints it's full path.
"""
import os

def find(directory,key_name):
    global files_raw
    files_raw = []
    go_deeper(directory)
    files_list = []
    for i in range(len(files_raw)):
        for j in range(len(files_raw[i][1])):
            folder = os.path.join(files_raw[i][0],files_raw[i][1][j])
            if key_name in folder:
                files_list.append(folder)
        for j in range(len(files_raw[i][2])):
            file = os.path.join(files_raw[i][0],files_raw[i][2][j])
            if key_name in file:
                files_list.append(file)
    del files_raw
    return files_list

def go_deeper(directory):
    global files_raw
    a = list(os.walk(directory))[0]
    files_raw.append(b)
    if len(a[1]) != 0:
        for i in range(len(a[1])):
            go_deeper(os.path.join(b[0],a[1][i]))

if __name__ == "__main__":
    print(find(input("[1/2]>>> "),input("[2/2]>>> ")))
