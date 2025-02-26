import platform
import subprocess
import os
import sys
from datetime import datetime
from setup import utils
from multiprocessing import Pool

# Set base path for executable compatibility
if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)  # Directory of the executable
else:
    BASE_PATH = os.getcwd()  # Current working directory in development


def run_command(args):
    terminal_number, system_platform, working_directory, command = args

    if system_platform == "Windows":
        subprocess.Popen(
            ["cmd", "/c", f"start cmd /c {command}"], shell=True
        )
    elif system_platform == "Linux":
        # Run in background for EC2 (no gnome-terminal)
        subprocess.Popen(f"cd {working_directory} && {command} &", shell=True)
    elif system_platform == "Darwin":
        apple_script = f'''
        tell application "Terminal"
            do script "cd {working_directory} && {command}; exit"
            delay 0.5 -- Ensure the command starts before we proceed                
        end tell
        '''
        subprocess.Popen(["osascript", "-e", apple_script])


def main():
    num_terminals = int(input("Enter the number of terminals to open: "))
    num_repetition = int(
        input("How many times do you want to run the test? (Max: 1000): "))

    # Create the log file when the run_university starts
    ad_click_log_file = utils.create_ad_click_log()

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    terminal_log_file = os.path.join(
        BASE_PATH, f"log/terminal_run_log_{timestamp}.log")

    # Ensure log directory exists
    os.makedirs(os.path.join(BASE_PATH, 'log'), exist_ok=True)

    # Prepare the command to execute
    system_platform = platform.system()
    working_directory = BASE_PATH  # Use BASE_PATH instead of os.getcwd()

    # New multiprocessing code
    with Pool(num_terminals) as pool:
        args = [
            (
                i + 1,
                system_platform,
                working_directory,
                f"{'python' if system_platform == 'Windows' else 'python3'} main.py {num_repetition} {i + 1} {ad_click_log_file} {terminal_log_file}"
            )
            for i in range(num_terminals)
        ]
        pool.map(run_command, args)


if __name__ == "__main__":
    main()
