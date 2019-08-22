#Splits 3DS' MPO into two JPGs with "_L" and "_R" postfix
#Because this program is too simple I release it under the CC0 license
#https://github.com/OSA413/Garbage

import sys

file_name = ""
if (len(sys.argv) == 1):
    print("3DS photo splitter by OSA413")
    print("Enter path to MPO file")
    file_name = input(">>> ")
else:
    file_name = sys.argv[1]

with open(file_name, "rb") as f:
    a = f.read()

split_ind = -1

for i in range(len(a) - 2):
    #This is Exif thing at the beginning of a JPG file
    if a[i] == 0x45 \
    and a[i+1] == 0x78 \
    and a[i+2] == 0x69 \
    and a[i+3] == 0x66 \
    and a[i+4] == 0x00 \
    and a[i+5] == 0x00:
        split_ind = i - 6
        if split_ind != 0:
            break

if split_ind > 0:
    with open(".".join(file_name.split(".")[:-1]) + "_L.JPG", "wb") as f:
        f.write(a[:split_ind])

    with open(".".join(file_name.split(".")[:-1]) + "_R.JPG", "wb") as f:
        f.write(a[split_ind:])
