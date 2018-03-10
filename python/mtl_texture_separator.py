"""
Copies textures that are used in MTL material file into a separated folder
"%file_name% used textures" where the MTL file is placed.
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
            separated_folder_name = str(f_name)+" used textures"
            if not os.path.exists(os.path.join(os.path.dirname(f_name),separated_folder_name)):
                os.makedirs(os.path.join(os.path.dirname(f_name),separated_folder_name))
            for i in range(len(texture_list)):
                texture = texture_list[i].split(" ")[1][:-1]
                shutil.copyfile(os.path.join(os.path.dirname(f_name),texture), os.path.join(os.path.dirname(f_name),separated_folder_name,texture))

            print("Done!")
        else:
            print("MTL file wasn't found")
    except:
        print("Error")
        print(sys.exc_info()[1])
