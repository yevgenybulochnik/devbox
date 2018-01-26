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
        self.name = cmd_name
        self.path = path
        self.type = type

    def run(self):
        start = datetime.datetime.now()
        if self.type == 'py':
            self.logger(self.name)
            exec(self.name)
        else:
            log = self.logger(self.name)
            proc = subprocess.Popen(
                self.name.split(),
                cwd=self.path,
                stdout=log,
                stderr=log
            )
            proc.wait()
        end = datetime.datetime.now()
        elasped_time = end - start
        self.time_logger(self.name, elasped_time)

    def logger(self, command):
        time_stamp = datetime.datetime.now()
        time_stamp_str = time_stamp.strftime('%m/%d/%y-%H:%M:%S:%f')
        command = command.split()
        if command[0] == 'sudo':
            command = command[1]
        else:
            command = command[0]
        spacer = '-' * 20
        log = open(p.join(LOG_DIR, 'dv_init.log'), 'a')
        log.write('\n' + spacer + command + spacer + time_stamp_str + '\n')
        log.flush()
        return log

    def time_logger(self, command, elapsed_time):
        command = command.split()
        if command[0] == 'sudo':
            command = command[1]
        else:
            command = command[0]
        spacer = '\n' + ('-' * 40) + '\n'
        log = open(p.join(LOG_DIR, 'dv_init_time.log'), 'a')
        log.write(spacer + command + '\n----' + str(elapsed_time) + '\n')
        log.flush()
        self.stamps.append(elapsed_time)


def get_time(commands):
    times = commands[0].stamps
    return sum(times, datetime.timedelta(0))


def main(py_version):
    if len(py_version) > 5:
        version = py_version[0:5]
        release = py_version[5:]
    else:
        version = py_version
        release = ''

    commands = [
        dv_command('wget https://www.python.org/ftp/python/{}/Python-{}.tgz -N'.format(version, version + release), SETUP_DIR),
        dv_command('tar -xf Python-{}.tgz'.format(version + release), SETUP_DIR),
        dv_command(p.join('.', SETUP_DIR, 'Python-{}'.format(version + release), 'configure'), SETUP_DIR),
        dv_command('rm -rf ' + SETUP_DIR),
        dv_command('print("Finish")', type='py')
    ]

    for cmd in commands:
        cmd.run()

    elapsed_time = get_time(commands)
    log = open(p.join(LOG_DIR, 'dv_init_time.log'), 'a')
    log.write(str(elapsed_time))
    print(elapsed_time)


main('3.6.4')
