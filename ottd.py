import subprocess
import argparse
import os
import tarfile
import pathlib
import gc

userpath = os.path.expanduser('~')
root_dir = f"{userpath}/ottd/"
instance_dir = f"{root_dir}/instances/"

parser = argparse.ArgumentParser()
parser.add_argument("-D", "--download")
parser.add_argument("-L", "--launch")
parser.add_argument("-U", "--uninstall")
parser.add_argument("-V", "--versions", action="store_true")
parser.add_argument("-Vv", "--version", action="store_true")
parser.add_argument("-R", "--repository")
parser.add_argument("-Rv", "--repositories", action="store_true")
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
    for version in pathlib.Path(instance_dir).iterdir():
        versions.append((str(version).split("/instances/")[1]))
    if printing:
        print("Installed OpenTTD versions:")
        for repo in repo_objects:
            print(f" - {repo.name}:")
            for version in versions:
                if str(version).split("-", 1)[0] == repo.name:
                    print(f"   * {str(version).split("-", 1)[1]}")
    else: 
        return versions

def repository_scan(printing=False):
    if printing:
        print("Configured repositories:")
        for repos in repo_objects:
            print(f" - {repos.name} ({repos.url})")
            for ver in repos.verified_vers:
                print(f"  * {ver}")
    else: 
        return reps

def download():
    wget_download = str(subprocess.run(["wget", download_repo], capture_output=True))
    
    if "saved" in wget_download:
        print("download successful")
    else:
        print("download failed")
        exit()
    with tarfile.open(download_filename, "r:xz") as downloaded_tar:
        downloaded_tar.extractall(path=instance_dir)
        print("untar successful")
        os.remove(download_filename)
        print("deleting tar sucessful")
    
    os.rename(f"{instance_dir}{download_filename.strip(".tar.xz")}", f"{instance_dir}{current_repo}-{download_ver}")
    print("folder rename successful")
    print("installation successful")

if f"{current_repo}-{download_ver}" not in version_scan() and args.download != None: # add scanning for if the version directory already exists
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