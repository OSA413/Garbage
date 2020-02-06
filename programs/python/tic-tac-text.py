#Tic Tac Toe text version by OSA413
#github.com/OSA413/tic-tac-text

__author__ = "OSA413"
__version__ = "1.0.1.20"
__license__ = "MIT License"

import random
import re
import sys
import os
import time
import urllib.request
import zipfile
from sys import exit

#input() UnicodeDecodeError "fix"
inputt = input
def input(x=""):
    try:
        return inputt(x)
    except EOFError:
        exit()
    except:
        return ""

#Shortcut of urllib.request.urlopen
def url_open(url , timeout = 0):
    return urllib.request.urlopen(url, timeout = timeout)

#Shortcut of random.randint
def rand(x):
    return random.randint(0,x)

global qpython
qpython = False
#AFAIK it is one of the ways to check if QPython is used
if "org.qpython.qpy3" in sys.prefix:
    qpython = True
    #It uses "tic-tac-text" folder in the root of sdcard
    qpython_path = "/sdcard/tic-tac-text/"
    if not os.path.exists(qpython_path):
        os.makedirs(qpython_path)
    os.chdir(qpython_path)
else:
    #By default it uses the same directory as the .py file in Windows, but Ubuntu saves the file in "/home/user_name" directory
    #The line below makes it to save files in the same directory as the .py file
    os.chdir(os.path.dirname(sys.argv[0]))

#Loads settings from settings file
def load_settings():
    global print_lines, print_delay, online_updating
    try:
        with open("settings.txt", "r") as f:
            #Print interval
            try:    print_lines = int(f.readline())
            except: print_lines = 2
            #Print delay
            try:    print_delay = float(f.readline())
            except: print_delay = 0.0
            #Online updating feature
            try:    online_updating = int(f.readline())
            except: online_updating = 1
    #If file doen't exist
    except:
        print_lines = 2
        print_delay = 0.0
        online_updating = 1
        
load_settings()

#Checks for available updates and updates the .py file
def online_update(mode="normal"):
    FILE_EXTENSION = os.path.splitext(sys.argv[0])[1][1:].lower()
    #If the online updating feature is on or forced update is selected from "Online Updating" menu
    if online_updating == 1 or mode == "forced":
        #Tries to connect to the server and read the version
        try:
            if mode == "forced": print("Connecting to the server...")
            else: print("Checking for updates...")
            if FILE_EXTENSION == "exe":
                new_version = url_open("https://github.com/OSA413/Tic-Tac-Text/releases/latest").geturl().split("/")[-1][1:]
            elif FILE_EXTENSION == "py" or qpython:
                repository = str(url_open("https://raw.githubusercontent.com/OSA413/Tic-Tac-Text/master/tic-tac-text.py", timeout = 5).read())
                new_version = re.search(r"__version__ = \"(\d|\.)+\"",repository).group()
                new_version = re.search(r"(\d|\.)+",new_version).group()

            new_version = new_version.split(".")
            #Rebuilds str to int for version on the server
            for i in range(len(new_version)):
                new_version[i] = int(new_version[i])
            if mode == "forced": print("Done!")
        #If program couldn't connect to the server, it sets new version at 0.0.0.0
        except:
            if mode == "forced": print("Failed...",sys.exc_info()[1])
            new_version = [0,0,0,0]
        #Rebuilds str to int for the current version
        current_version = __version__.split(".")
        for i in range(len(current_version)):
            current_version[i] = int(current_version[i])

        #compares both versions
        update_available = False
        for i in range(len(new_version)):
            if new_version[i] > current_version[i]:
                update_available = True
            if new_version[i] < current_version[i]:
                break

        #If a new version is available or update is forced
        if update_available or (mode == "forced" and new_version != [0,0,0,0]):
            #At the start of the program it offers to update to the newest version
            if mode == "normal":
                print("A new version of this game is available. Do you want to update it right now?")
                user_input = input("[Y/N]>>> ")
            else:
                user_input = ""
            #If user preferred to update at the start
            if user_input.lower() == "y" or mode == "forced":
                if FILE_EXTENSION == "exe":
                    #Downloading windows archive
                    print("Downloading archive...")
                    with open("tmp_arc.zip","wb") as f:
                        the_url = url_open("https://github.com/OSA413/Tic-Tac-Text/releases/latest").geturl().replace("tag","download")+"/Tic-Tac-Text_win.zip"
                        f.write(url_open(the_url).read())

                    tmp_folder = "tmp_"+str(rand(1000000))

                    print("Extracting archive...")
                    tpm_arc = zipfile.ZipFile("tmp_arc.zip", 'r')
                    tpm_arc.extractall(tmp_folder)
                    tpm_arc.close()


                    print("Starting Update Finalizer...")
                    with open("update_finalizer.bat","w") as f:
                        text = "TASKKILL /IM "+str(os.path.basename(sys.argv[0]))+" /F"
                        text += "\nMOVE \""+str(os.path.join(os.getcwd(),tmp_folder,"*"))+"\" \""+str(os.getcwd())+"\""
                        text += "\nRMDIR \""+str(os.path.join(os.getcwd(),tmp_folder))+"\""
                        text += "\nDEL \""+str(os.path.join(os.getcwd(),"tmp_arc.zip"))+"\""
                        text += "\nSTART \"\" \""+str(os.path.join(os.getcwd(),"Tic-Tac-Text.exe"))+"\""
                        text += "\nDEL \""+str(os.path.join(os.getcwd(),"update_finalizer.bat"))+"\""
                        f.write(text)

                    os.startfile(os.path.join(os.getcwd(),"update_finalizer.bat"))
                    exit()
                    
                else:
                    if qpython:
                        """
                        QPython is an interpretor of Python 3 on Android.
                        sys.argv[0] returns "", os.getcwd() returns "/"
                        So, I can't detect where the script is run from.
                        An updated version of the game will be placed in "Programs>Scripts" menu.
                        """
                        file_name = "/sdcard/qpython/scripts3/tic-tac-text "+".".join(list(map(str,new_version)))+".py"
                    else:
                        file_name = str(sys.argv[0])
                    if mode == "forced": print("Downloading the game file...")
                    urllib.request.urlretrieve("https://raw.githubusercontent.com/OSA413/Tic-Tac-Text/master/tic-tac-text.py", file_name)
                    if mode == "forced": print("Done!")
                    #If user uses Windows, the program will restart automatically
                    if sys.platform == "win32":
                        os.startfile(file_name)
                    #Else user will be offered to restart the program manually
                    else:
                        add_text = ""
                        if qpython:
                            add_text = "Run file \"tic-tac-text "+".".join(list(map(str,new_version)))+".py\"\n"
                        input("The game has been updated to the newest version. Please, restart the game.\n"+str(add_text))
                    exit()
            else:
                del repository
                print("\n"*(print_lines-1))

online_update()

#The grid mask that is used to print the game grid
grid_mask = "\n  1 2 3\n #-#-#-#\nA|A1|A2|A3|\n #-#-#-#\nB|B1|B2|B3|\n #-#-#-#\nC|C1|C2|C3|\n #-#-#-#"

#Prints or returns the grid
def print_grid(mode=0):
    text = grid_mask
    for i in range(3):
        for j in range(3):
            text = text.replace("ABC"[i]+str(j+1), grid_table[i][j])
    if mode == 0:
        print(text)
    elif mode == 1:
        return text

#Mirrors the grid
def mirror_grid():
    global grid_table
    for i in range(3):
        temp = grid_table[i][0]
        grid_table[i][0] = grid_table[i][2]
        grid_table[i][2] = temp

#Rotates the grid at 90° to the left
def rotate_grid():
    global grid_table
    grid_tmp = [[" "," "," "],[" "," "," "],[" "," "," "]]
    for i in range(3):
        for j in range(3):
            grid_tmp[2-j][i]=grid_table[i][j]
    grid_table = grid_tmp

#Sets up a new game, cleans up history of steps
def new_game(enemy=0):
    global grid_table, game_status, bot_status, game_step, winner, game_steps, all_possible_steps, grid_history
    #This is the steps data [A_line,B_line,C_line]
    grid_table = [[" "," "," "],[" "," "," "],[" "," "," "]]
    game_status = None
    game_step = 1
    winner = 0
    #bot_status: 0 is human vs. human, 1 is easy, 2 is normal, 3 is hard
    bot_status = int(enemy)
    #The below variables are used for game_dump
    game_steps = []
    all_possible_steps = []
    grid_history = []

#Converts coordinates to int for the player
def coord2num(step):
    try:
        #Finds A, B, or C (line) in the input
        if "A" in step:
            step_n = 0
            step = step.replace("A","")
        elif "B" in step:
            step_n = 1
            step = step.replace("B","")
        elif "C" in step:
            step_n = 2
            step = step.replace("C","")
        step = int(step)-1 + step_n*3
        #If the coordinate is not empty, returns "Occupied"
        if not grid_table[step // 3][step % 3] == " ":
            step = "Occupied"
    except:
        step = None
    finally:
        return step

#Converts int to coordinate for the player
def num2coord(step):
    return str(["A","B","C"][int(step) // 3])+str(int(step) % 3 + 1)

#Checks if there's 3 in a row on the grid
def check():
    global winner
    #This if for switching between X and O
    for j in ("X","O"):
        for i in range(3):
            #In-column row
            if grid_table[i-1][0] == j and grid_table[i-1][1] == j and grid_table[i-1][2] == j:
                winner = j
            #In-line row
            if grid_table[0][i-1] == j and grid_table[1][i-1] == j and grid_table[2][i-1] == j:
                winner = j
        #Diagonal top left to bottom right
        if grid_table[0][0] == j and grid_table[1][1] == j and grid_table[2][2] == j:
            winner = j
        #Diagonal top right to bottom left
        if grid_table[0][2] == j and grid_table[1][1] == j and grid_table[2][0] == j:
            winner = j
    #Checks if all the coordinates are not empty. Draw
    if not grid_table[0][0] == " " and not grid_table[0][1] == " " and not grid_table[0][2] == " " and not grid_table[1][0] == " " and not grid_table[1][1] == " " and not grid_table[1][2] == " " and not grid_table[2][0] == " " and not grid_table[2][1] == " " and not grid_table[2][2] == " " and winner == 0:
        winner = None

#Changes the current room
def goto_room(x):
    global room
    room = x

#Allows human to make a step
def player_step(mark):
    global turn, game_step, dif
    step = 0
    turn = "player"
    while turn == "player" and room == "grid":
        #If the coordinate is wrong (something like "E102","B9", or "G3")
        if step == None:
            print("You have written a wrong coordinate. Please choose the correct coordinate.")
        #If the coordinate is not empty
        elif step == "Occupied":
            print("The coordinate is occupied. Please choose another coordinate.")
        step = input(">>> ").upper()

        #Backs to the main menu
        if step.lower() == "exit":
            goto_room("title")
            break
        #Restarts (re-enters new game)
        elif step.lower() == "restart":
            new_game(dif)
            break

        step = coord2num(step)
        #If step is not None (incorrect input) or str (coordinate is occupied)
        if type(step) == int:
            grid_table[step // 3][step % 3] = mark
            game_step += 1
            turn = "bot"
            game_steps.append(num2coord(step))
            all_possible_steps.append("")

#The AI of bot is below
def bot_step():
    global bot_mark, bot_status, hum_mark, game_step
    possible_steps = []

    #Normal difficulty
    if bot_status >= 2:
        for k in [bot_mark,hum_mark]:
            if k == hum_mark and not possible_steps == []:
                break
            #Bot checks if it can complete 3 in a row.
            for i in range(3):
                turns_check = [k,k," ",k,k]
                for j in range(3):
                    #Checks columns
                    if grid_table[i][0] == turns_check[j] and grid_table[i][1] == turns_check[j+1] and grid_table[i][2] == turns_check[j+2]:
                        possible_steps.append(i*3+2-j)
                    #Checks lines
                    if grid_table[0][i] == turns_check[j] and grid_table[1][i] == turns_check[j+1] and grid_table[2][i] == turns_check[j+2]:
                        possible_steps.append(3-(j-1)*3+i)

                #Checks diagonal top left to bottom right
                if grid_table[0][0] == turns_check[i] and grid_table[1][1] == turns_check[i+1] and grid_table[2][2] == turns_check[i+2]:
                    possible_steps.append(4-(i-1)*4)
                #Checks diagonal top right to bottom left
                if grid_table[0][2] == turns_check[i] and grid_table[1][1] == turns_check[i+1] and grid_table[2][0] == turns_check[i+2]:
                    possible_steps.append(6-i*2)


    #Hard difficulty
    #Bot makes a "win-only" step
    if bot_status == 3 and possible_steps == []:
        if bot_mark == "X":
            #Each step has its own good steps
            if game_step == 1:
                possible_steps = [0,2,4,6,8]
            else:
                if game_step == 3:
                    #Sometimes bot mirrors and rotates the grid to find a good step
                    for mirror in range(2):
                        for rotation in range(4):
                            if grid_table[1][1] == "X":
                                if grid_table[0][0] == "O":
                                    possible_steps.append([8,mirror,rotation])
                                elif grid_table[0][1] == "O":
                                    possible_steps.append([6,mirror,rotation])
                                    possible_steps.append([8,mirror,rotation])
                            elif grid_table[0][0] == "X":
                                if grid_table[0][1] == "O" or grid_table[0][2] == "O" or grid_table[1][2] == "O":
                                    possible_steps.append([6,mirror,rotation])
                                elif grid_table[2][2] == "O":
                                    possible_steps.append(4)
                                elif grid_table[1][1] == "O":
                                    possible_steps.append([8,mirror,rotation])
                            rotate_grid()
                        mirror_grid()
                elif game_step == 5:
                    for mirror in range(2):
                        for rotation in range(4):
                            if grid_table[0][0] == "X" and grid_table[1][0] == " " and grid_table[2][0] == "X" and grid_table[2][1] == " " and grid_table[2][2] == " ":
                                possible_steps.append([8,mirror,rotation])
                            rotate_grid()
                        mirror_grid()
        elif bot_mark == "O":
            if game_step == 2:
                if grid_table[1][1] == " ":
                    possible_steps = [4]
                elif grid_table[1][1] == "X":
                    possible_steps = [0,2,6,8]
            if game_step == 4:
                for mirror in range(2):
                    for rotation in range(4):
                        if grid_table[0][1] == "X" and grid_table[1][2] == "X" and grid_table[0][2] == " ":
                            possible_steps = [[0,mirror,rotation],[2,mirror,rotation],[8,mirror,rotation]]
                        elif grid_table[1][1] == "X" and grid_table[0][0] == "X" and grid_table[2][2] == "O":
                            possible_steps = [[2,mirror,rotation],[6,mirror,rotation]]
                        elif grid_table[0][0] == "X" and grid_table[1][1] == "O" and grid_table[2][2] == "X":
                            possible_steps = [1,3,5,7]
                        rotate_grid()
                    mirror_grid()

    #Decoding the steps if the grid was mirrored or rotated at hard difficulty.
    for i in range(len(possible_steps)):
        if type(possible_steps[i]) == list:
            #The encoded coordinates are [coord,rotation,mirror]
            step = possible_steps[i]
            #Rotation to the right
            for r in range(step[2]):
                if step[0] == 0:    step[0] = 2
                elif step[0] == 1:    step[0] = 5
                elif step[0] == 2:    step[0] = 8
                elif step[0] == 5:    step[0] = 7
                elif step[0] == 8:    step[0] = 6
                elif step[0] == 7:    step[0] = 3
                elif step[0] == 6:    step[0] = 0
                elif step[0] == 3:    step[0] = 1
            #Mirror again
            if step[1] == 1:
                #If it is on the left side, move to the right
                if (int(step[0])+3)%3 == 0:
                    step[0] += 2
                #If on the right side, move left
                elif (int(step[0])+3)%3 == 2:
                    step[0] -= 2
            possible_steps[i] = step[0]


    #Normal difficulty again
    #If there's no good steps, bot continues the row
    if bot_status >= 2 and possible_steps == []:
        for i in range(3):
            turns_check = [" "," ",bot_mark," "," "]
            for j in range(3):
                #Checks lines
                if grid_table[i][0] == turns_check[j] and grid_table[i][1] == turns_check[j+1] and grid_table[i][2] == turns_check[j+2]:
                    if j == 0:
                        possible_steps += [i*3, i*3+1]
                    elif j == 1:
                        possible_steps += [i*3, i*3+2]
                    elif j == 2:
                        possible_steps += [i*3+1, i*3+2]
                #Checks columns
                if grid_table[0][i] == turns_check[j] and grid_table[1][i] == turns_check[j+1] and grid_table[2][i] == turns_check[j+2]:
                    if j == 0:
                        possible_steps += [i, 3+i]
                    elif j == 1:
                        possible_steps += [i, 6+i]
                    elif j == 2:
                        possible_steps += [3+i, 6+i]
            #Checks diagonal top left to bottom right
            if grid_table[0][0] == turns_check[i] and grid_table[1][1] == turns_check[i+1] and grid_table[2][2] == turns_check[i+2]:
                if i == 0:
                    possible_steps += [0, 4]
                if i == 1:
                    possible_steps += [0, 8]
                if i == 2:
                    possible_steps += [4, 8]
            #Checks diagonal top right to bottom left
            if grid_table[0][2] == turns_check[i] and grid_table[1][1] == turns_check[i+1] and grid_table[2][0] == turns_check[i+2]:
                if i == 0:
                    possible_steps += [2, 4]
                if i == 1:
                    possible_steps += [2, 6]
                if i == 2:
                    possible_steps += [4, 6]

    #Easy difficulty
    #Steps at a random coordinate
    if possible_steps == []:
        num = rand(8)
        while not grid_table[num // 3][num % 3] == " ":
            num = rand(8)
        possible_steps.append(num)

    #Makes a list of unique coordinates
    possible_steps = list(set(possible_steps))

    #Chooses one of some possible steps
    num = rand(len(possible_steps)-1)
    num = possible_steps[num]
    grid_table[num // 3][num % 3] = bot_mark
    game_step += 1
    #This is for the history of a game
    game_steps.append(num2coord(num))
    for i in range(len(possible_steps)):
        possible_steps[i] = num2coord(possible_steps[i])
    all_possible_steps.append(possible_steps)

#Saves settings of the game
def save_settings():
    global print_lines, print_delay, online_updating
    with open("settings.txt", "w") as f:
        f.write(str(print_lines)+"\n"   #Print interval
                +str(print_delay)+"\n"  #Print delay
                +str(online_updating))  #Online updating feature

#Prints a message with input for settings
def call_settings(call):
    #[1] Print delay
    if call == "print_delay":
        global print_delay
        text_s = "" if print_delay == 1 else "s"
        print("Write text printing delay in seconds that you want (current is "+str(print_delay)+" second(s))".replace("(s)",text_s))
        user_input = input("[No more than 2 seconds are allowed]>>> ")
        #Replaces commas to dots
        user_input = user_input.replace(",",".")
        while True and user_input != "":
            try:
                #No more than 2 seconds
                if float(user_input) <= 2:
                    print_delay = float(user_input)
                    save_settings()
                else:
                    raise TypeError
                break
            except:
                user_input = input("Your input is not correct. Try again>>> ")
    #[2] Print lines
    if call == "print_lines":
        global print_lines
        text_s = "" if print_lines == 1 else "s"
        print("Write text printing interval in lines that you want (current is "+str(print_lines)+" line(s))".replace("(s)",text_s))
        user_input = input("[No more than 30 lines are allowed]>>> ")
        #Replaces commas to dots
        user_input = user_input.replace(",",".")
        while True and user_input != "":
            try:
                #No more than 30 lines
                if float(user_input) <= 30:
                    print_lines = int(user_input)
                    save_settings()
                else:
                    raise TypeError
                break
            except:
                user_input = input("Your input is not correct. Try again>>> ")
    #[3] On/off online updating
    if call == "online_updating":
        global online_updating
        text_s = "enabled" if online_updating == 1 else "disabled"
        print("Do you want to get online updating? When a new version is available, you'll be notified at startup. Currently online updating is "+str(text_s)+".")
        user_input = input("[Y/N]>>> ").lower()
        if user_input == "y":
            online_updating = 1
        elif user_input == "n":
            online_updating = 0
        save_settings()

#Creates a file with the current game information
def dump_game():
    global grid_table, grid_history
    #Time of creation of the dump
    #year/month/day hh:mm:ss
    ctime = (str(time.localtime()[0])+"/"\
            +str(time.localtime()[1])+"/"\
            +str(time.localtime()[2])+" "\
            +str(time.localtime()[3])+":"\
            +str(time.localtime()[4])+":"\
            +str(time.localtime()[5]))

    #The header of the dump
    game_dump_text = ""
    game_dump_text += "Tic-Tac-Text game dump\n"
    game_dump_text += "Game version: "+str(__version__)+"\n"
    game_dump_text += "\n"
    game_dump_text += "Dump created at "+str(ctime)+"\n"*2

    game_dump_text += "#####################\n"
    game_dump_text += "Game information:\n\n"
    #If the game is not human vs. human, shows human's mark and bot's mark
    if bot_status != 0:
        game_dump_text += "Human plays as "+str(hum_mark)+", bot plays as "+str(bot_mark)+"\n"
    game_dump_text += "Game's difficulty: "+str(bot_status)+"\n\n"

    for i in range(game_step-1):
        game_dump_text += "===Game step: "+str(i+1)+"===\n"
        #If the game is not human vs. human
        if bot_status != 0:
            if hum_mark == "X" and i % 2 == 0:
                game_dump_text += "Human's turn"+"\n"
            elif hum_mark == "O" and i % 2 == 1:
                game_dump_text += "Human's turn"+"\n"
            else:
                game_dump_text += "Bot's turn"+"\n"
                #All the possible steps that bot could do
                game_dump_text += "Bot's possible steps: "+str(all_possible_steps[i])+"\n"
        else:
            if i % 2 == 0:
                game_dump_text += "X's turn"+"\n"
            elif i % 2 == 1:
                game_dump_text += "O's turn"+"\n"

        #The coordinate that player did a step at
        game_dump_text += "Step at "+str(game_steps[i])+"\n"
        #The grid data BEFORE the player did a step
        game_dump_text += str(grid_history[i])+"\n"
        game_dump_text += "\n"

    game_dump_text += "===End===\n"

    #Who wins?
    if winner == None: game_dump_text += "Draw"
    #If human vs. human
    if bot_status == 0:
        if winner == "X": game_dump_text += "X wins"
        elif winner == "O": game_dump_text += "O wins"
    #If human vs. bot
    else:
        if winner == bot_mark: game_dump_text += "Bot wins"
        elif winner == hum_mark: game_dump_text += "Human wins"

    game_dump_text += "\n"
    #The last-step grid data
    game_dump_text += str(grid_history[-1])+"\n"
    game_dump_text += "#####################\n"

    #Saves game dump in the "year.month.day hh-mm-ss.txt" file
    dump_file = "game_dump "+str((ctime.replace("/",".")).replace(":","-"))+".txt"
    with open(dump_file, "w") as f:
        f.write(game_dump_text)

    print("\nThe game dump has been saved in \""+str(dump_file)+"\" file.")
        

def main():
    global room, bot_mark, hum_mark, turn, print_lines, print_delay, online_updating, dif
    room = "title"
    user_input = ""

    load_settings()
    #Prints the header of the game
    print("\tTic Tac Text by OSA413")
    print("\tVersion: "+str(__version__))
    while True:
        if room == "title":
            print("***Main Menu***")
            print("[1] Play")
            print("[2] Options")
            print("[3] Online Updating")
            print("[4] Exit")
            user_input = input(">>> ")

            if user_input == "1":
                goto_room("ng_menu")
            elif user_input == "2":
                goto_room("options")
            elif user_input == "3":
                goto_room("online_updating")
            elif user_input == "4":
                goto_room("exit")

        elif room == "ng_menu":
            print("***New game menu***")
            print("[1] Play with a bot")
            print("[2] Play with a partner")
            print("[3] Back")
            user_input = input(">>> ")

            if user_input == "1":
                goto_room("bot_setup")
            elif user_input == "2":
                goto_room("grid")
                new_game()
                dif = 0
            elif user_input == "3":
                goto_room("title")

        elif room == "bot_setup":
            dif = 0
            print("***Choose bot's difficulty***")
            print("[1] Easy")
            print("[2] Normal")
            print("[3] Hard")
            print("[4] Back")
            user_input = input(">>> ")

            if user_input == "1":
                goto_room("mark_sel")
                dif = 1
            elif user_input == "2":
                goto_room("mark_sel")
                dif = 2
            elif user_input == "3":
                goto_room("mark_sel")
                dif = 3
            elif user_input == "4":
                goto_room("ng_menu")
                
        elif room == "mark_sel":
            print("Select your mark")
            user_input = input("[X/O/BACK]>>> ")
            if user_input.lower() == "x":
                hum_mark = "X"
                bot_mark = "O"
                new_game(dif)
                goto_room("grid")
            elif user_input.lower() == "o":
                hum_mark = "O"
                bot_mark = "X"
                new_game(dif)
                goto_room("grid")
            elif "b" in user_input.lower():
                goto_room("bot_setup")

        elif room == "options":
            print("***Options***")
            print("[1] Print delay")
            print("[2] Print interval")
            print("[3] On/off online updating")
            print("[4] Back")
            user_input = input(">>> ")

            if user_input == "1":
                call_settings("print_delay")
            elif user_input == "2":
                call_settings("print_lines")
            elif user_input == "3":
                call_settings("online_updating")
            elif user_input == "4":
                goto_room("title")

        elif room == "grid":
            if winner == 0:
                if bot_status == 0:
                    check()
                    if winner == 0:
                        grid_history.append(print_grid(1))
                        print_grid()
                        player_step("X")
                    check()
                    if winner == 0:
                        grid_history.append(print_grid(1))
                        print_grid()
                        player_step("O")
                else:
                    if hum_mark == "X":
                        check()
                        print_grid()
                        if winner == 0:
                            grid_history.append(print_grid(1))
                            player_step(hum_mark)
                        check()
                        if winner == 0 and game_step !=1:
                            grid_history.append(print_grid(1))
                            bot_step()
                    elif hum_mark == "O":
                        if winner == 0:
                            grid_history.append(print_grid(1))
                            bot_step()
                        check()
                        print_grid()
                        if winner == 0:
                            grid_history.append(print_grid(1))
                            player_step(hum_mark)
                        check()
            else:
                grid_history.append(print_grid(1))
                if winner == None: print("Nobody wins. Draw.")
                if bot_status == 0:
                    if winner == "X": print("X wins!")
                    elif winner == "O": print("O wins!")
                else:
                    if winner == bot_mark: print("Bot wins. You lose.")
                    elif winner == hum_mark: print("You win!")
                print_grid()
                print("\nDo you want to play again?")
                user_input = input("[Y/N/SETTINGS/GD]>>> ")
                if user_input.lower() == "y":
                    new_game(bot_status)
                if user_input.lower() == "n":
                    goto_room("title")
                if "s" in user_input.lower():
                    goto_room("ng_menu")
                if user_input.lower() == "gd":
                    dump_game()

        elif room == "online_updating":
            print("***Online Updating Menu***")
            print("[1] On/off online updating")
            print("[2] Forced update")
            print("[3] Exit")
            user_input = input(">>> ")

            if user_input == "1":
                call_settings("online_updating")
            elif user_input == "2":
                online_update("forced")
            elif user_input == "3":
                goto_room("title")

        elif room == "exit":
            print("Are you sure you want to exit this game?")
            user_input = input("[Y/N]")
            if "y" in user_input.lower() or user_input == "":
                exit()
            else:
                goto_room("title")
        #Prints with delay in seconds
        time.sleep(print_delay)
        #Prints interval between the "screens"
        if print_lines > 0:
            print("\n"*(print_lines-1))

if __name__ == "__main__":
    main()
