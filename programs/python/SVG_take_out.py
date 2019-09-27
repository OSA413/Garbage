#This thing will take all svg files from a file (e.g. otf)
#Because this program is too simple I release it under the CC0 license
#https://github.com/OSA413/Garbage

import sys

#The nodes of SVG's XML
SVG_START = b"\x3C\x73\x76\x67"
SVG_END   = b"\x3C\x2F\x73\x76\x67"

file_name = ""
if (len(sys.argv) == 1):
    print("SVG take out by OSA413")
    print("Enter path to a file")
    file_name = input(">>> ")
else:
    file_name = sys.argv[1]

with open(file_name, "rb") as f:
    a = f.read()

pointer_svg_start = 0
pointer_svg_end   = 0

for i in range(len(a)):
    if pointer_svg_start <= pointer_svg_end:
        if a[i:i+len(SVG_START)] == SVG_START:
            pointer_svg_start = i
    else:
        if a[i:i+len(SVG_END)] == SVG_END:
            for j in range(len(a[i:])):
                if a[i+j] == 0x3E:
                    pointer_svg_end = i + j + 1
                    break
            
            if pointer_svg_start <= pointer_svg_end:
                with open("file"+str(i)+".svg", "wb") as f:
                    f.write(a[pointer_svg_start:pointer_svg_end])
