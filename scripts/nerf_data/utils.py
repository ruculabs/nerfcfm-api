import os
import subprocess

def ensure_dir(directory):
    """Ensure a directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def is_command_available(command):
    """Check if a command-line tool is available."""
    try:
        subprocess.run([command, '--help'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
