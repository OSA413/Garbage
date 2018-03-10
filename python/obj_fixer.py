"""
This program fixes .obj files that contain "#" at the end of the lines
    e.g. "v 0 0.05 5.599998 #1"
and commas instead of dots in .mtl files.
    e.g. "d 0,69803923368454"

This may be usefull if you use old SADXLVL and SADXMDL by MainMemory to rip
Sonic Adventure DX models and levels.

How to use: enter the full path to the .obj and .mtl files without the file
extension.
    e.g.
        if the full path to the model is "D:\game\models\test.obj" and
        "D:\game\models\test.mtl", enter "D:\game\models\test".

If .obj or .mtl is missed, it will be skipped.

Update 0:
Now this program can add missed "d 1" and "Tr 1" lines in MTL files if you use
SAMDL (by MainMemory), so the models will not look too darker and "edgy".
"""
import re
import sys
import os

while True:
    try:
        f_name = input(">>> ")

        if os.path.exists(str(f_name)+".obj"):
            with open(str(f_name)+".obj","r") as f:
                model = f.read()

            #I know that a better way exists, but I didn't know about it when I was writting it.
            garbage_list = re.findall(r"#.+?\n",model)

            print(len(garbage_list))
            last_progress = None
            for i in range(len(garbage_list)):
                model = model.replace(garbage_list[i],"\n")
                #something like progre ssbar
                if int((i/len(garbage_list)*10)) != last_progress:
                    last_progress = int((i/len(garbage_list)*10))
                    print(last_progress)

            with open(str(f_name)+".obj","w") as f:
                f.write(model)
        else:
            print("OBJ file wasn't found")

        if os.path.exists(str(f_name)+".mtl"):
            with open(str(f_name)+".mtl","r") as f:
                material = f.read()

            #Change this line if you want to fix translucency of material or to not
            fix_d_Tr = None
            with open(str(f_name)+".mtl","w") as f:
                material = material.replace(",",".")
                if material.count("newmtl ") != material.count("Tr "):
                    if fix_d_Tr == None:
                        fix_d_Tr = input("Fix translucency?\n[Y|N]>>> ") in ["y","Y"]
                    if fix_d_Tr:
                        material = material.replace("\nillum","\nd 1\nTr 1\nillum")
                f.write(material)
        else:
            print("MTL file wasn't found")

        print("Done!")

    except:
        print("Error")
        print(sys.exc_info()[1])
