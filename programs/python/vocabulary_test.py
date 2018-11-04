#Test your vocabulary!
#TODO: add second separator for words with the same meaning.
"""
This program is designed to show you random words on one language, you have to write them in another language.
The words are defined in a separated file and are splitted by a symbol.
This is at least the third version of this kind of programs.
This also supports QPython 3
"""
import os, sys, random

print("Made by OSA413 under MIT License.")
print("github.com/OSA413\n")

vocabulary_file = "vocabulary.txt"
main_separator = "-"
progress_file = ""

#input() UnicodeDecodeError "fix"
inputt = input
def input(x=""):
    try:
        return inputt(x)
    except EOFError:
        exit()
    except:
        return ""

def load():
    global progress_file
    file = ""
    lst_all = []
    if os.path.isfile("/sdcard/" + vocabulary_file):
        file = "/sdcard/" + vocabulary_file
    elif os.path.isfile(os.path.join(os.path.dirname(__file__), vocabulary_file)):
        file = os.path.join(os.path.dirname(__file__), vocabulary_file)
    
    if file == "": return

    progress_file = file + "_progress.txt"

    with open(file,"r") as f:
        text0 = f.read()
        
    text1 = ""
    if os.path.isfile(progress_file):
        with open(progress_file,"r") as f:
            text1 = f.read()
    
    lst0 = text0.split("\n")
    lst1 = text1.split("\n")
    
    for i in range(len(lst0)):
        prog = 0
        ttt = lst0[i].split(main_separator)
        if len(ttt) != 2:
            continue
        prog = int(lst1[i])
        
        lst_all.append([ttt[0], ttt[1], prog])
    
    return lst_all

def save(lst_all):
    with open( progress_file ,"w") as f:
        f.write("\n".join([str(x[2]) for x in lst_all]))

main_list = load()

index_list = []

for i in range(len(main_list)):
    index_list += [i]*(101-main_list[i][2])
    
random.shuffle(index_list)

print(len(main_list)/len(index_list)*100)

for i in index_list:
    word_index = random.randint(0,1)
    print(main_list[i][word_index])
    user_input = input(">>> ")
    
    correct = False
    if user_input == main_list[i][1-word_index]:
        correct = True
        
    if not correct and user_input != "":
        len0 = len(main_list[i][1-word_index])
        len1 = len(user_input)
        sum0 = 0
        sum1 = 0
        
        for j in main_list[i][1-word_index]:
            sum0 += ord(j.lower())
        for j in user_input:
            sum1 += ord(j.lower())
            
            
        if len1 > len0:
            len0 += len1
            len1 = len0 - len1
            len0 -= len1
        
        if sum1 > sum0:
            sum0 += sum1
            sum1 = sum0 - sum1
            sum0 -= sum1
            
        rsltt = ((sum1/len1)/(sum0/len0)*(len1/len0))**2
        
        print(rsltt)
        if rsltt > 0.98: correct = True

    dif = (3*correct-2)*(main_list[i][2]//10+1)

    if user_input == "" or user_input == main_list[i][word_index]: dif = 0
    
    main_list[i][2] += dif
    
    if dif>0: dif="+"+str(dif)
    else: dif = str(dif)
    
    if main_list[i][2] < 0: main_list[i][2] = 0
    if main_list[i][2] > 100: main_list[i][2] = 100
    
    if correct:
        print("Right!")
    else:
        print("Wrong")
    print("\t",main_list[i][1-word_index])
        
    print("Word Progress: ", main_list[i][2], "("+str(dif)+")")

    print("="*25,"\n")
    save(main_list)
    
