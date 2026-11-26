from cmd_handler import run_shell
import os

def download(url: str, path=None):
    if run_shell("wget") == 404:
        print("Falling back to curl: wget not in PATH")
        curl_download(url, path)
    else:
        wget_download(url, path)

def wget_download(url: str, path=None):
    if path != None:
        wget = run_shell(f"wget -P {path} {url}")
    else:
        wget = run_shell(f"wget {url}")
        if "saved" in wget:
            print("download successful")
        else:
            exit("download failed")

def curl_download(url: str, path=None):
    if path != None:
        curl = run_shell(f"curl -L -o {path} {url}")
    else:
        curl = run_shell(f"curl -L -O {url}")
        filename = url.split("/")[-1]
        try:
            if os.path.getsize(filename) > 0:
                print("download successful")
            else:
                exit("download failed")
        except FileNotFoundError:
            exit("download failed")