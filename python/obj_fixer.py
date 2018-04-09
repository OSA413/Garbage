"""
This program fixes .obj files that contain "#" at the end of the lines
    e.g. "v 0 0.05 5.599998 #1"
and commas instead of dots in .mtl files.
    e.g. "d 0,69803923368454"

How to use: enter the full path to the .obj and .mtl files without the file
extension.
    e.g.
        if the full path to the model is "D:\game\models\test.obj" and
        "D:\game\models\test.mtl", enter "D:\game\models\test".

If .obj or .mtl is missed, it will be skipped.
"""

def fix_obj(path):
    with open(str(path)+".obj","r") as f:
        model = f.read()

    #This way is faster than using regex
    fixed_model = model.split("\n")
    for i in range(len(fixed_model)):
        if "#" in fixed_model[i]:
            fixed_model[i] = fixed_model[i][:fixed_model[i].index("#")]

    with open(str(path)+".obj","w") as f:
        f.write("\n".join(fixed_model))

def fix_mtl(path, fix_translucency = False):
    with open(str(path)+".mtl","r") as f:
        material = f.read()

    material = material.replace(",",".")
    if fix_translucency:
        if material.count("Tr ") == 0 and material.count("newmtl "):
            for parameter in ["Map_Kd","illum","Ns","Ks","Kd","Ka"]:
                if material.count(str(parameter)+" ") == material.count("newmtl "):
                    material = material.replace("\n"+str(parameter),"\nd 1\nTr 1\n"+str(parameter))
                    break
        
    with open(str(path)+".mtl","w") as f:
        f.write(material)

def fix(path, fix_translucency = False):
    fix_obj(path)
    fix_mtl(path, fix_translucency)

if __name__ == "__main__":
    fix(input(">>> "),input("Fix translucency?\n[Y|N]>>> ") in ["y","Y"])
