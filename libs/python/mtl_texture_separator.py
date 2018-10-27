"""
Copies textures that are used in MTL material file into a separated folder
"%file_name% used textures" where the MTL file is placed.
Usage: enter the full path to the MTL file.
"""
import re
import os
import shutil

def get_textures(mtl_file):
    with open(mtl_file,"r") as f:
        material = f.read()
        
    texture_list = list(set(re.findall(r"Map_Kd .+?\n",material)))
    for i in range(len(texture_list)):
        texture_list[i] = texture_list[i][7:-1]

    return texture_list

def separate(mtl_file,separated_folder = None):
    if separated_folder == None:
        separated_folder = os.path.join(os.path.dirname(mtl_file),str(mtl_file)+" used textures")
    if not os.path.exists(separated_folder):
        os.makedirs(separated_folder)

    texture_list = get_textures(mtl_file)
    for i in range(len(texture_list)):
        shutil.copyfile(os.path.join(os.path.dirname(mtl_file),texture_list[i]), os.path.join(separated_folder,texture_list[i]))

if __name__ == "__main__":
    separate(input(">>> "))
