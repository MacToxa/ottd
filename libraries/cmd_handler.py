import subprocess

def run_shell(cmd: str):
    command = cmd.split(" ")
    try:
        result = subprocess.run(command, capture_output=True, text=True)
    except FileNotFoundError:
        return 404
    else:
        return result