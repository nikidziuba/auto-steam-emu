import subprocess
import os
import glob
import shutil
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.simpledialog import askinteger
import sys

def main():
    Tk().withdraw()
    game_folder, game_exec = get_info()
    steamless(game_exec)

    goldberg(game_folder)

# PyInstaller compability
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def steamless(file: str):
    file_name = os.path.splitext(file)[0]
    file_path = os.path.dirname(file)

    sl_path = resource_path("./bin/Steamless.CLI.exe")
    try:
        subprocess.run([sl_path, "--quiet ", file], check=True, stdout=subprocess.PIPE)
        os.rename(file, os.path.join(file_path, file_name + ".bak.exe"))
        os.rename(os.path.join(file + ".unpacked.exe"), file)
    except:
        print("Steamless returned an error, either you selected a wrong file or the game doesn't use protection")


# TODO: Auto detect APPID
def goldberg(folder_path: str):
    glb = glob.glob(folder_path + "/**/steam_api.dll", recursive=True)

    if len(list(glb)) == 0:
        glb = glob.glob(folder_path + "/**/steam_api64.dll", recursive=True)
    if len(list(glb)) == 0:
        print("Couldn't find steam api dll, you have to replace it manually")
        return 1
    dll = glb[0]
    dll_name = os.path.splitext(os.path.split(dll)[1])[0]
    dll_path = os.path.dirname(dll)

    if os.path.isfile(os.path.join(dll_path, "steam_appid.txt")):
        appid = 0
    else:
        appid = str(askinteger(title="INPUT", prompt="App Id:"))

    os.rename(dll, os.path.join(dll_path, dll_name + ".bak.dll"))

    gldbrg_path = resource_path("./bin/" + dll_name + ".dll")
    shutil.copy(gldbrg_path, dll)
    if appid != 0:
        with open(dll_path + '/steam_appid.txt', 'w') as f:
            f.write(appid)

def  get_info():
    game_path = askdirectory(title="Game Folder:")
    game_exec = askopenfilename(filetypes=[("Executables", "*.exe")], initialdir=game_path)

    return game_path, game_exec

if __name__ == '__main__':
    main()
