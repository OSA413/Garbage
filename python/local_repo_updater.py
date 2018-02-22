"""
Downloads repositories from GitHub
To download a repo, create a directory with the same name as the repo
Place this python script file near to the directory
    e.g. file structure
        /myrepo/repo
        /myrepo/local_repo_updater.py

The repository will be downloaded from GitHub and placed in the diretory
Note: it deletes old files that are not in the current repository
"""
import zipfile
import urllib.request
import os
import shutil
import sys

#change it to your GitHub username or the program will ask to input it every time.
user = None

#input() UnicodeDecodeError "fix"
inputt = input
def input(x=""):
    try:
        return inputt(x)
    except EOFError:
        exit()
    except:
        return ""

#By default it uses the same directory as the .py file in Windows, but Ubuntu saves the file in "/home/user_name" directory
#The line below makes it to save the file in the same directory as the .py file
try:
    os.chdir(sys.argv[0][:len(sys.argv[0])-len(sys.argv[0].split("/")[-1])])
except:
    os.chdir(sys.argv[0][:len(sys.argv[0])-len(sys.argv[0].split("\\")[-1])])

def open_page(url):
    return urllib.request.urlopen(url)

if user == None:
    user = input("Enter your GitHub username\n")

#makes a list of all directories (repos)
print("Searching folders...")
repo = list(filter(lambda dr: os.path.isdir(dr), os.listdir(os.getcwd())))
print("Found "+str(len(repo))+" folders")

print("Checking user existance...")
user_exists = False
try:
    resource = open_page("https://github.com/"+str(user))
    print("User exists.")
    user_exists = True
except:
    print(sys.exc_info()[1])

if user_exists:
    for i in range(len(repo)):
        #downloading archive
        print(" Downloading "+str(repo[i])+" repository...")
        try:
            resource = open_page("https://github.com/"+str(user)+"/"+str(repo[i])+"/archive/master.zip")
            with open("tmp_arc", "wb") as f:
                f.write(resource.read())

            #delete the old directory
            shutil.rmtree(repo[i])
            
            #extracting downloaded acrhive to the new directory
            arc_zip = zipfile.ZipFile("tmp_arc")
            arc_zip.extractall(os.getcwd())
            arc_zip.close()

            #renaming "repo-master" to "repo"
            os.rename(str(repo[i])+"-master",repo[i])
            print(str(repo[i])+" extracted.")
        except:
            print(sys.exc_info()[1])

    try:
        os.remove("tmp_arc")
    except:
        pass
input("\nPress Enter to exit.")
exit()
