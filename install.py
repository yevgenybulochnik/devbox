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

    deb_dep = [
        'build-essential',
        'libncursesw5-dev',
        'libssl-dev',
        'libc6-dev',
        'libsqlite3-dev',
        'tk-dev',
        'libbz2-dev',
        'zlib1g-dev',
        'vim'
    ]

    commands = [
        dv_command('add-apt-repository ppa:jonathonf/vim -y'),
        dv_command('apt update'),
        dv_command('apt install -y ' + ' '.join(deb_dep)),
        dv_command('wget https://www.python.org/ftp/python/{}/Python-{}.tgz -N'.format(version, version + release), SETUP_DIR),
        dv_command('tar -xf Python-{}.tgz'.format(version + release), SETUP_DIR),
        dv_command(p.join('.', SETUP_DIR, 'Python-{}'.format(version + release), 'configure'), SETUP_DIR),
        dv_command('make', SETUP_DIR),
        dv_command('make altinstall', SETUP_DIR),
        dv_command('wget https://deb.nodesource.com/setup_8.x', SETUP_DIR),
        dv_command('bash setup_8.x', SETUP_DIR),
        dv_command('apt install -y nodejs', SETUP_DIR),
        dv_command('npm install -g pm2'),
        dv_command('rm -rf ' + SETUP_DIR),
        dv_command('pip3.6 install .'),
    ]

    for cmd in commands:
        print('\nRunning: ' + cmd.name)
        cmd.run()
        print('Elapsed Time: ' + str(get_time(commands)))

    elapsed_time = get_time(commands)
    log = open(p.join(LOG_DIR, 'dv_init_time.log'), 'a')
    log.write(str(elapsed_time))
    print('\nFinished')
    print(elapsed_time)


main('3.6.4')
