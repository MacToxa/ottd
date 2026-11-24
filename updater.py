import os
import subprocess
import argparse
# path variables
from paths import soundfont_dir, soundfont_path, soundfont_license_path

# updater variables
soundfont_link = "https://github.com/mactoxa/ottd/raw/refs/heads/main/soundfont/GeneralUser-GS.sf2"
soundfont_license_link = "https://github.com/mactoxa/ottd/raw/refs/heads/main/soundfont/LICENSE.txt"

parser = argparse.ArgumentParser()
parser.add_argument("--setup", action="store_true", help="Set up everything (Arch Linux only)")
parser.add_argument("--update", action="store_true", help="Update everything")
args = parser.parse_args()

if args.setup:
    timidity_install = os.system('sudo pacman -S --noconfirm timidity++')
    if timidity_install == 0:
        print("OTTD: Installed timidity")
    else:
        exit("OTTD: Failed to install timidity")
    
    wget_install = os.system('sudo pacman -S --noconfirm wget')
    if wget_install == 0:
        print("OTTD: Installed wget")
    else:
        exit("OTTD: Failed to install wget")
    
    if not os.path.exists(soundfont_path):
        wget_download = str(subprocess.run(["wget", "-P", soundfont_dir, soundfont_link,], capture_output=True))
        if "saved" in wget_download:
            print("OTTD: Soundfont download successful")
        else:
            exit("OTTD: Soundfont download failed")
    else:
        print("OTTD: Soundfont already exists")
    
    if not os.path.exists(soundfont_license_path):
        wget_download = str(subprocess.run(["wget", "-P", soundfont_dir, soundfont_license_link], capture_output=True))
        if "saved" in wget_download:
            print("OTTD: Soundfont license download successful")
        else:
            exit("OTTD: Soundfont license download failed")
    else:
        print("OTTD: Soundfont license already exists")