import os
import shutil
import time
from simple_term_menu import TerminalMenu


def progress_percentage(perc, width=None):
    # This will only work for python 3.3+ due to use of
    # os.get_terminal_size the print function etc.

    FULL_BLOCK = '█'
    # this is a gradient of incompleteness
    INCOMPLETE_BLOCK_GRAD = ['░', '▒', '▓']

    assert(isinstance(perc, float))
    assert(0. <= perc <= 100.)
    # if width unset use full terminal
    if width is None:
        width = os.get_terminal_size().columns
    # progress bar is block_widget separator perc_widget : ####### 30%
    max_perc_widget = '[100.00%]'  # 100% is max
    separator = ' '
    blocks_widget_width = width - len(separator) - len(max_perc_widget)
    assert(blocks_widget_width >= 10)  # not very meaningful if not
    perc_per_block = 100.0/blocks_widget_width
    # epsilon is the sensitivity of rendering a gradient block
    epsilon = 1e-6
    # number of blocks that should be represented as complete
    full_blocks = int((perc + epsilon)/perc_per_block)
    # the rest are "incomplete"
    empty_blocks = blocks_widget_width - full_blocks

    # build blocks widget
    blocks_widget = ([FULL_BLOCK] * full_blocks)
    blocks_widget.extend([INCOMPLETE_BLOCK_GRAD[0]] * empty_blocks)
    # marginal case - remainder due to how granular our blocks are
    remainder = perc - full_blocks*perc_per_block
    # epsilon needed for rounding errors (check would be != 0.)
    # based on reminder modify first empty block shading
    # depending on remainder
    if remainder > epsilon:
        grad_index = int((len(INCOMPLETE_BLOCK_GRAD) * remainder)/perc_per_block)
        blocks_widget[full_blocks] = INCOMPLETE_BLOCK_GRAD[grad_index]

    # build perc widget
    str_perc = '%.2f' % perc
    # -1 because the percentage sign is not included
    perc_widget = '[%s%%]' % str_perc.ljust(len(max_perc_widget) - 3)

    # form progressbar
    progress_bar = '%s%s%s' % (''.join(blocks_widget), separator, perc_widget)
    # return progressbar as string
    return ''.join(progress_bar)


def copy_progress(copied, total):
    print('\r' + progress_percentage(100*copied/total, width=30), end='')


def copyfile(src, dst, *, follow_symlinks=True):
    """Copy data from src to dst.

    If follow_symlinks is not set and src is a symbolic link, a new
    symlink will be created instead of copying the file it points to.

    """
    if shutil._samefile(src, dst):
        raise shutil.SameFileError("{!r} and {!r} are the same file".format(src, dst))

    for fn in [src, dst]:
        try:
            st = os.stat(fn)
        except OSError:
            # File most likely does not exist
            pass
        else:
            # XXX What about other special files? (sockets, devices...)
            if shutil.stat.S_ISFIFO(st.st_mode):
                raise shutil.SpecialFileError("`%s` is a named pipe" % fn)

    if not follow_symlinks and os.path.islink(src):
        os.symlink(os.readlink(src), dst)
    else:
        size = os.stat(src).st_size
        with open(src, 'rb') as fsrc:
            with open(dst, 'wb') as fdst:
                copyfileobj(fsrc, fdst, callback=copy_progress, total=size)
    return dst


def copyfileobj(fsrc, fdst, callback, total, length=16*1024):
    copied = 0
    while True:
        buf = fsrc.read(length)
        if not buf:
            break
        fdst.write(buf)
        copied += len(buf)
        callback(copied, total=total)


def copy_with_progress(src, dst, *, follow_symlinks=True):
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src))
    copyfile(src, dst, follow_symlinks=follow_symlinks)
    shutil.copymode(src, dst)
    return dst

################################################################
# Thanks to Martin Pieters and flutefreak7 in stackoverflow
# for tracking progress and progress bar when copying with shutil
################################################################


os.system("clear")

UMM_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager')
UMM_MOD_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager\mods')
DATA_ARC_DUMP_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\atmosphere\contents\01006A800016E000\romfs')
DATA_ARC_BACKUP_PATH = os.path.expandvars(r'%APPDATA%\yuzu\sdmc\UltimateModManager\data_arc_backup')

read_secs = 1

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
print("When finished, press enter below to continue:")

TerminalMenu(["Dump completed"]).show()
print("\nAlright! Let's continue.")
time.sleep(read_secs)

# Step 2, create folders and backup for data.arc
print("Step 2: Let's now check and create then necessary folders.\n")
time.sleep(read_secs)
print("Let's check for the Ultimate Mod Manager directory...")

# Checks if the directory exists
if(os.path.isdir(UMM_PATH)):
    print("Ultimate Mod Manager directory exists! Great.")
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

    try:
        os.mkdir(UMM_MOD_PATH)
    except OSError as err:
        print("Whoops! For some reason, we couldn't create the necessary folders.")
        print("Here is the problem:")
        print(err.message)
    else:
        print("Successfully created mods folder! Creating an extra folder for data.arc backup...")

    try:
        os.mkdir(DATA_ARC_BACKUP_PATH)
    except OSError as err:
        print("Whoops! For some reason, we couldn't create the necessary folders.")
        print("Here is the problem:")
        print(err.message)
    else:
        print("Successfully created data.arc backup folder.")
        time.sleep(read_secs-1)
        print("Moving on...")


# Step 3, backing up data.arc
print("Step3: Creating backup of data.arc...")
time.sleep(read_secs-1)
print("This may take a while...")
copy_with_progress(DATA_ARC_DUMP_PATH, DATA_ARC_BACKUP_PATH)
print("Done! Awesome.")
