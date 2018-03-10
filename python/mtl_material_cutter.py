"""
Some model converters may leave unused materials in MTL files.
This program leave only used materials from OBJ file in MTL file.

How to use: enter the full path to the .obj and .mtl files without the file
extension.
    e.g.
        if the full path to the model is "D:\models\test.obj" and
        "D:\models\test.mtl", enter "D:\models\test".
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
            material_list = list(set(re.findall(r"usemtl .+?\n",model)))
            for i in range(len(material_list)):
                material_list[i] = material_list[i].split(" ")[1]

            print(str(len(material_list))+" materials in OBJ file")

            if os.path.exists(str(f_name)+".mtl"):
                with open(str(f_name)+".mtl","r") as f:
                    material = f.read()

                save_materials = []
                print(str(material.count("newmtl"))+" materials in MTL file")
                if material.count("newmtl") != len(material_list):
                    print("Searching unused materials...")
                    materials_used = material.split("newmtl ")[1:]
                    for i in range(len(materials_used)):
                        for j in material_list:
                            if materials_used[i].startswith(j):
                                save_materials.append([i,j])
                    material = ""
                    print("Cutting unused materials...")
                    for i in save_materials:
                        material += "newmtl "+str(materials_used[i[0]])

                    with open(str(f_name)+".mtl","w") as f:
                        f.write(material)
                else:
                    print("Nothing to cut!")
            else:
                print("MTL file wasn't found")
        else:
            print("OBJ file wasn't found")

        print("Done!")

    except:
        print("Error")
        print(sys.exc_info()[1])
