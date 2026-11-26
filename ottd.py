import subprocess
import argparse
import os
import tarfile
import pathlib
import gc
import shutil
# path variables
from paths import *
# libraries
import libraries.networking as net
from libraries.cmd_handler import run_shell

parser = argparse.ArgumentParser()
parser.add_argument("-D", "--download", help="Download OpenTTD versions; use the repository-version format")
parser.add_argument("-L", "--launch", help="Launch OpenTTD versions; use the repository-version format")
parser.add_argument("-U", "--uninstall", help="Remove installed OpenTTD versions; use the repository-version format")
parser.add_argument("-V", "--versions", action="store_true", help="List installed OpenTTD versions")
parser.add_argument("-Vv", "--version", action="store_true", help="Show the version and feature information")
parser.add_argument("-S", "--search", help="Fetch information on OpenTTD versions; use the repository-version format")
parser.add_argument("-R", "--repositories", action="store_true", help="List the available repositories and the versions they contain for sure")
parser.add_argument("--setup", action="store_true", help="Set up everything (Arch Linux only)")
args = parser.parse_args()

current_repo = None
download_ver = None
if args.download != None:
    try:
        current_repo = str(args.download).split("-", 1)[0]
        download_ver = str(args.download).split("-", 1)[1]
    except IndexError:
        print("Download argument only supports this format: repo-version")
        exit()

class Repository:
  def __init__(self, name:str, url:str, filename:str, verified_vers:list):
    self.name = name
    self.url = url
    self.filename = filename
    self.verified_vers = verified_vers

openttd = Repository(
    "openttd",
    f"https://cdn.openttd.org/openttd-releases/{download_ver}/openttd-{download_ver}-linux-generic-amd64.tar.xz", 
    f"openttd-{download_ver}-linux-generic-amd64.tar.xz",
    [
    "15.3",
    "14.1"
    ]
)
citymania = Repository(
    "citymania",
    f"https://citymania.org/static/files/client/citymania-client-{download_ver}-linux-generic-amd64.tar.xz", 
    f"citymania-client-{download_ver}-linux-generic-amd64.tar.xz",
    [
    "15.3",
    "13.4"
    ]
)
jgrpp = Repository(
    "jgrpp",
    f"https://github.com/JGRennison/OpenTTD-patches/releases/download/jgrpp-0.{download_ver}/openttd-jgrpp-0.{download_ver}-linux-generic-amd64.tar.xz", 
    f"openttd-jgrpp-0.{download_ver}-linux-generic-amd64.tar.xz",
    [
    "73.5",
    "73.4"
    ]
)

repo_objects = []
download_filename = None
download_repo = None
download_verified = None
for obj in gc.get_objects():
    if isinstance(obj, Repository):
        repo_objects.append(obj)
        if current_repo == obj.name: 
            download_repo = obj.url
            download_filename = obj.filename
            download_verified = obj.verified_vers

def version_scan(printing=False):
    versions = []
    try:
        for version in pathlib.Path(instance_dir).iterdir():
            versions.append(str(version).split("/instances/")[1])
    except FileNotFoundError:
        versions = []
    if printing:
        print("Installed OpenTTD versions:")
        if versions != []:
            for repo in repo_objects:
                print(f" - {repo.name}:")
                for version in versions:
                    if version.split("-", 1)[0] == repo.name:
                        print(f"   * {version.split("-", 1)[1]}")
        else:
            print(" - No OpenTTD versions installed.")
    else: 
        return versions

def repository_scan(printing=False):
    if printing:
        print("Configured repositories:")
        for repo in repo_objects:
            print(f" - {repo.name} ({repo.url})")
            for ver in repo.verified_vers:
                print(f"  * {ver}")
    else: 
        return repo_objects

def download():
    net.download(download_repo)
    with tarfile.open(download_filename, "r:xz") as downloaded_tar:
        downloaded_tar.extractall(path=instance_dir)
        print("untar successful")
        os.remove(download_filename)
        print("deleting tar sucessful")
    
    os.rename(f"{instance_dir}{download_filename.strip(".tar.xz")}", f"{instance_dir}{current_repo}-{download_ver}")
    print("folder rename successful")
    print("installation successful")

if f"{current_repo}-{download_ver}" not in version_scan() and args.download != None:
    if download_ver in download_verified:
        download()
    else:
        print("The file has not been verified to exist")
        response = input("Try to download? (y/n) ")
        if response == "y" or response == "Y":
            download()
elif f"{current_repo}-{download_ver}" in version_scan() and args.download != None:
    print("Version already downloaded")

if args.launch != None:
    os.system(f"{instance_dir}{args.launch}/openttd")

if args.versions:
    version_scan(True)

if args.repositories:
    repository_scan(True)

if args.setup:
    userinput = input("The setup script requires elevation. Do you want to run it? Y/N ")
    if userinput == "y" or userinput == "Y":
        run_shell(f"python3 {alt_root_dir}updater.py --setup")

if args.uninstall != None:
    try: 
        shutil.rmtree(f"{instance_dir}{args.uninstall}")
    except FileNotFoundError: 
        print("Version not found")
    else:
        print("Version uninstalled successfully")

if args.version:
    print("                                       OTTD 1.0")
    print()
    print("                                       Features:")
    print("""                   (planned features are denoted by an asterisk)

    - Downloading and installing OpenTTD official and community-made versions
    - Launching OpenTTD versions
    - Uninstalling OpenTTD versions
    * Instancing OpenTTD options and BaNaNaS content
    * Providing a configuration file for custom repositories
    * Browsing BaNaNaS and managing its content through the terminal
    * Fetching information on OpenTTD versions
    """)