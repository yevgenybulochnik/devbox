#!/usr/bin/env python3
import os
import subprocess
import os.path as p
import datetime

SCRIPT_DIR = p.dirname(p.abspath(__file__))
SETUP_DIR = p.join(SCRIPT_DIR, 'setup')
LOG_DIR = p.join(SCRIPT_DIR, 'logs')

os.makedirs(SETUP_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

class dv_command:
    stamps = []
    def __init__(self, cmd_name, path=SCRIPT_DIR, type='sh'):
        self.cmd= cmd_name
        self.path = path
        self.type = type
    def run(self):
        if self.type == 'py':
            exec(self.cmd)
        else:
            log = self.logger(self.cmd)
            proc = subprocess.Popen(
                self.cmd.split(),
                cwd=self.path,
                stdout=log,
                stderr=log
            )
            proc.wait()
        self.time_logger()
    def logger(self, command):
        command = command.split()
        if command[0] == 'sudo':
            command = command[1]
        else:
            command = command[0]
        spacer = '-' * 20
        log = open(p.join(LOG_DIR, 'dv_init.log'), 'a')
        log.write('\n' + spacer + command + spacer + '\n')
        log.flush()
        return log
    def time_logger(self):
        self.stamps.append('test')



commands = [
    dv_command('wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz -N', SETUP_DIR),
    dv_command('tar -xf Python-3.6.3.tgz', SETUP_DIR),
    dv_command(p.join('.', SETUP_DIR,'Python-3.6.3', 'configure'), SETUP_DIR),
    dv_command('rm -rf ' + SETUP_DIR)
]

for cmd in commands:
    cmd.run()

print(commands[0].stamps)
