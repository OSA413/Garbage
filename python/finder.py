#Checks if file exists; can be found by the full name or a part of the name; if file exists, prints it's name (not full path to the file)
import os
import re
found = False

while True:
    print("Enter directory")
    directory = input()

    exists = False

    while True:
        print("\nEnter file name")
        file = input()
        print()
        files = []
        if file == ":back":
            break
        try:
            i = 0
            for d, dirs, filess in os.walk(directory):
                files += filess
            
        except:
            pass

        for i in files:
            try:
                re.search(file,i).group()
                found = True
                print(i)
            except:
                pass
        print()
        if found:
            print("File exists")
            found = False
            pass
        else:
            print("File doesn't exist")
