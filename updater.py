import os
import subprocess
from ottd import soundfont_dir

# updater variables
soundfont_link = "https://github.com/kruant/ottd/raw/refs/heads/main/soundfont/GeneralUser-GS.sf2"
soundfont_license_link = "https://github.com/kruant/ottd/raw/refs/heads/main/soundfont/LICENSE.txt"

timidity_install = os.system('pacman -S --noconfirm timidity++')
if timidity_install == 0:
    print("OTTD: Installed timidity")
else:
    exit("OTTD: Failed to install timidity")
wget_install = os.system('pacman -S --noconfirm wget')
if wget_install == 0:
    print("OTTD: Installed wget")
else:
    exit("OTTD: Failed to install wget")
wget_download = str(subprocess.run(["wget", "-P", soundfont_dir, soundfont_link,], capture_output=True))
if "saved" in wget_download:
    print("OTTD: Soundfont download successful")
else:
    exit("OTTD: Soundfont download failed")
wget_download = str(subprocess.run(["wget", "-P", soundfont_dir, soundfont_license_link], capture_output=True))
if "saved" in wget_download:
    print("OTTD: Soundfont license download successful")
else:
    exit("OTTD: Soundfont license download failed")