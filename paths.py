import os
import pwd
import pathlib

real_user = os.environ.get("SUDO_USER") 

if real_user:
    userpath = pwd.getpwnam(real_user).pw_dir
else:
    userpath = os.path.expanduser('~')

# path variables
root_dir = f"{userpath}/ottd/"
alt_root_dir = f"{os.path.dirname(os.path.realpath(__file__))}/"
instance_dir = f"{root_dir}/instances/"
soundfont_dir = f"{root_dir}/soundfont/"
soundfont_path = f"{soundfont_dir}GeneralUser-GS.sf2"