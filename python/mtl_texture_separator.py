"""
Copies textures that are used in MTL material file into a separated folder
"Used textures" where the MTL file is placed.
Usage: enter the full path to the MTL file.
"""
import re
import sys
import os
import shutil

while True:
    try:
        f_name = input(">>> ")

        if os.path.exists(f_name):
            with open(f_name,"r") as f:
                material = f.read()
            print(os.path.dirname(f_name))

            texture_list = list(set(re.findall(r"Map_Kd .+?\n",material)))
            print(str(len(texture_list))+" textures in MTL file")
            print("Separating textures...")
            if not os.path.exists(os.path.join(os.path.dirname(f_name),"Used textures")):
                os.makedirs(os.path.join(os.path.dirname(f_name),"Used textures"))
            for i in range(len(texture_list)):
                texture = texture_list[i].split(" ")[1][:-1]
                shutil.copyfile(os.path.join(os.path.dirname(f_name),texture), os.path.join(os.path.dirname(f_name),"Used textures",texture))

        else:
            print("MTL file wasn't found")
        print("Done!")
    except:
        print("Error")
        print(sys.exc_info()[1])
