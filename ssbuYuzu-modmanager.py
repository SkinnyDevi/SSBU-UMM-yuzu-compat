import os
import time
import json
from tqdm import tqdm

os.system("clear")

UMM_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager')
UMM_MOD_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager\mods')
DATA_ARC_DUMP_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\atmosphere\contents\01006A800016E000\romfs')
DATA_ARC_BACKUP_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager\data_arc_backup')

read_secs = 2

print("Welcome to the Mod Manager Tool for Yuzu SSBU and Ultimate Mod Manager!")
time.sleep(read_secs)

# Step 1, dump data.arc to directory
print("Step 1: Dump data.arc to the Yuzu directory.\n")
time.sleep(read_secs)
print("To do this:")
time.sleep(read_secs)
print("- Open Yuzu Emulator and locate Super Smash Bros Ultimate Mod Manager")
time.sleep(read_secs)
print("- Right click the game, and select \"Dump\", and select \"Dump ROMFS to SDMC\"")
time.sleep(read_secs+1)
print("- Choose \"Base\" option and then \"Full\" option \n")
time.sleep(read_secs)
print("Leave the program running, it'll take about 10-30 minutes (Depending on your computer). \n")
time.sleep(read_secs)
print("When finished, the program will continue:")

dataArcFound = True
while dataArcFound:
    if os.path.isfile(DATA_ARC_DUMP_PATH+'\data.arc'):
        dataArcFound = False
    else:
        print("Waiting for data.arc file")
        time.sleep(read_secs)
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
    print("Seems you have a data.arc backup folder in UMM, interesting...\n We'll need that!")
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
    defaultConfig = {}
    defaultConfig["has_run_setup"] = True
    defaultConfig["has_custom_mod_folder"] = False
    print("Generating and writing config.json...")
    try:
        config.write(json.dumps(defaultConfig))
    except OSError as e:
        print("Woah! We couldn't make a config file.")
        print("Here is what's stopping us from continuing...")
        print(e.message)
    else:
        print("Okay! We're good to go. Let's continue.")
