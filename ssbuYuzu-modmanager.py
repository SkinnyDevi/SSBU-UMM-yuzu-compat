import os
from os import walk
import time
import json
from tqdm import tqdm
from PyInquirer import prompt

os.system("cls")

UMM_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager')
UMM_MOD_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager\mods')
DATA_ARC_DUMP_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\atmosphere\contents\01006A800016E000\romfs')
DATA_ARC_BACKUP_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager\data_arc_backup')
CONFIG_PATH = DATA_ARC_BACKUP_PATH+'\config.json'

read_secs = 2

print("Welcome to the Mod Manager Tool for Yuzu SSBU and Ultimate Mod Manager!")
time.sleep(read_secs)


def runSetup():

    # Step 1, dump data.arc to directory
    print("Step 1: Dump data.arc to the Yuzu directory.\n")
    time.sleep(read_secs)
    print("To do this:")
    time.sleep(read_secs)
    print("- Open Yuzu Emulator and locate Super Smash Bros Ultimate")
    time.sleep(read_secs)
    print("- Right click the game, and select \"Dump\", and select \"Dump ROMFS to SDMC\"")
    time.sleep(read_secs+1)
    print("- Choose \"Base\" option and then \"Full\" option \n")
    time.sleep(read_secs)
    print("Leave the program running, it'll take about 10-30 minutes (Depending on your computer). \n")
    time.sleep(read_secs)
    print("When Yuzu tells you that it has finished dumping, continue:")

    # 17252303608 bytes -> data.arc file size tested locally
    dataArcFound = True
    while dataArcFound:
        a = input("Press {Enter} to continue when the dump has finished...")
        if os.path.isfile(DATA_ARC_DUMP_PATH+'\data.arc') and (os.path.getsize(DATA_ARC_DUMP_PATH+'\data.arc') >= 17252303608):
            dataArcFound = False
        else:
            print("Whoops! It seems the file is not correct or the file has not finished importing, try again.")
    print("\nAlright! Let's continue.")
    time.sleep(read_secs)


    # Step 2, create folders and backup for data.arc
    print("Step 2: Let's now check and create then necessary folders.\n")
    time.sleep(read_secs)
    print("Let's check for the Ultimate Mod Manager directory...")

    # Checks if the directory exists
    is_umm_path = False
    is_umm_mod_path = False
    is_umm_dataarc_backup_path = False

    if (os.path.isdir(UMM_PATH)):
        is_umm_path = True
    if (os.path.isdir(UMM_MOD_PATH)):
        is_umm_mod_path = True
    if (os.path.isdir(DATA_ARC_BACKUP_PATH)):
        is_umm_dataarc_backup_path = True

    if (is_umm_path):
        print("Ultimate Mod Manager directory exists! Great.")
        time.sleep(read_secs-1)
    else:
        print("Oh, theres, nothing. Don\'t worry, we'll be creating everything for you.")
        try:
            os.mkdir(UMM_PATH)
        except OSError as err:
            print("Whoops! For some reason, we couldn't create the necessary folders.")
            print("Here is the problem:")
            print(err.message)
        else:
            print("Successfully created Ultimate Mod Manager folder, now adding mods folder...")
            time.sleep(read_secs-2)

    if (is_umm_mod_path):
        print("Awesome! You seem to have the mods directory correctly setup.")
        time.sleep(read_secs-1)
    else:
        try:
            os.mkdir(UMM_MOD_PATH)
        except OSError as err:
            print("Whoops! For some reason, we couldn't create the necessary folders.")
            print("Here is the problem:")
            print(err.message)
        else:
            print("Successfully created mods folder! Creating an extra folder for data.arc backup...")
            time.sleep(read_secs-2)

    if (is_umm_dataarc_backup_path):
        print("Seems you have a data.arc backup folder in UMM, interesting...\nWe'll need that!")
        time.sleep(read_secs-1)
        print("Moving on...")
    else:
        try:
            os.mkdir(DATA_ARC_BACKUP_PATH)
        except OSError as err:
            print("Whoops! For some reason, we couldn't create the necessary folders.")
            print("Here is the problem:")
            print(err.message)
        else:
            print("Successfully created data.arc backup folder.")
            time.sleep(read_secs-1)
            print("Moving on...\n")


    # Step 3, backing up data.arc
    if (os.path.isfile(DATA_ARC_BACKUP_PATH+'\data.arc')):
        print("Skipping Step 3: You already have a backup of the data.arc file in the correct folder!")
    else:
        print("Step3: Creating backup of data.arc...")
        time.sleep(read_secs-1)
        print("This may take a while...")
        with open(DATA_ARC_DUMP_PATH+'\data.arc', 'rb') as dataArc:
            with open(DATA_ARC_BACKUP_PATH+'\data.arc', 'wb') as newDataArc:
                fileSize = os.path.getsize(DATA_ARC_DUMP_PATH+'\data.arc')
                pbar = tqdm(total=fileSize, unit='B', unit_scale=True)
                for i in dataArc:
                    newDataArc.write(i)
                    pbar.update(len(i))
                pbar.close()
                newDataArc.close()
                dataArc.close()
        print("Done! Awesome.")

    # Step 4, generate a config.json
    print("We're nearly there, just generating a config file...")
    with open(DATA_ARC_BACKUP_PATH+'\config.json', 'w') as config:
        defaultConfig = {
            "has_run_setup": True,
            "has_custom_mod_folder": False
        }
        print("Generating and writing config.json...")
        try:
            json.dump(defaultConfig, config, indent=2)
        except OSError as e:
            print("Woah! We couldn't make a config file.")
            print("Here is what's stopping us from continuing...")
            print(e.message)
        else:
            print("Okay! We're good to go. Let's continue.")
            time.sleep(read_secs)


# Options: Add mods, install & uninstall mods and remove completely
# Finally, setup a custom mod folder #

defaultChoice = [{
    'type': 'list',
    'name': 'yes_no_choice',
    'message': '',
    'choices': ['Yes', 'No']
}]


def menu():
    os.system('cls')
    notQuit = True
    print("Hey There! Welcome to the main menu.")
    menuOptions = [
        {
            'type': 'list',
            'name': 'tool_main_menu',
            'message': 'Choose between the options using the arrows, and press enter to choose the option:',
            'choices': ["Install Mods", "Uninstall Mods", "Setup Custom Mod Folder (Unavailable ATM)"]
        }
    ]
    answer = prompt(menuOptions)["tool_main_menu"]
    print(answer)
    if (answer == menuOptions[0]['choices'][0]):
        install()
    elif (answer == menuOptions[0]["choices"][1]):
        uninstall()
    elif (answer == menuOptions[0]["choices"][2]):
       setupCustomModFolder()


def restoreDataArc_Backup():
    print("OPTION UNDER DEVELOPMENT")


def install():
    print("OPTION UNDER DEVELOPMENT")


def setupCustomModFolder():
    print("OPTION UNDER DEVELOPMENT")


def uninstall():
    os.system('cls')
    folderPath = UMM_MOD_PATH
    dirnames = next(walk(folderPath), (None, [], None))[1]
    modUninstall = [{
        'type': 'list',
        'name': 'mod_uninstall',
        'message': 'Choose a mod to uninstall:',
        'choices': []
    }]
    modUninstall[0]['choices'].append("-#- CANCEL -#-")
    for mod in dirnames:
        modUninstall[0]['choices'].append(mod)
    toUninstall = prompt(modUninstall)
    if toUninstall['mod_uninstall'] == "-#- CANCEL -#-":
        os.system('cls')
        menu()
    else:
        defaultChoice[0]['message'] = f"You chose to uninstall {toUninstall['mod_uninstall']} mod, continue?"
        confirmUninstall = prompt(defaultChoice)['yes_no_choice']
        print(f"You chose {confirmUninstall}")
        if confirmUninstall == 'Yes':
            if (os.path.exists(folderPath+"/"+toUninstall['mod_uninstall'])):
                os.rmdir(folderPath+"/"+toUninstall['mod_uninstall'])
                menu()
            else:
                print("Folder no longer exists")
        else:
            menu()


# SCRIPT PROCESS STARTS HERE
if (os.path.isdir(DATA_ARC_BACKUP_PATH)):
    config = None
    with open(CONFIG_PATH, 'r') as configFile:
        config = json.loads("".join(configFile.readlines()))
        print("HAS RUN SETUP - " + str(config['has_run_setup']))
    if (config['has_run_setup']):
        menu()
    else:
        runSetup()
        menu()
else:
    runSetup()
    menu()