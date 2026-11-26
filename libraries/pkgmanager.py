import platform
from cmd_handler import run_shell

def identify_os():
    global system
    if "Darwin" in platform.version(): system = "macOS"
    if "Ubuntu" in platform.version(): system = "Ubuntu"
    return system

def pkg_download(package: str) -> bool:
    identify_os()
    if system == "macOS":
        if run_shell("brew") == 404:
            print("No package manager found!")
            return False
        
pkg_download("a")