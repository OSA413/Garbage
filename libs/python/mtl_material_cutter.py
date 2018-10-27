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

def get_materials(path):
    with open(str(path)+".obj","r") as f:
        model = f.read()

    materials_list = list(set(re.findall(r"usemtl .+?\n",model)))
    for i in range(len(materials_list)):
        materials_list[i] = materials_list[i][7:-1]

    return materials_list

def cut(path):
    materials_list = get_materials(path)

    with open(str(path)+".mtl","r") as f:
        material = f.read()

    if material.count("newmtl") != len(materials_list):
        save_materials = []
        materials_used = material.split("newmtl ")[1:]
        for i in range(len(materials_used)):
            for j in materials_list:
                if materials_used[i].startswith(str(j)+"\n"):
                    save_materials.append([i,j])

        material = ""
        for i in save_materials:
            material += "newmtl "+str(materials_used[i[0]])

        with open(str(path)+".mtl","w") as f:
            f.write(material)

if __name__ == "__main__":
    cut(input(">>> "))
