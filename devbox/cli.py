"""
Devbox is a python command line application that assists in provisioning a development server.

Usage:
    devbox <command> [<args>...]
    devbox (-h | --help)

Options:
    -h --help

Commands:
    a2config
    adduser
    setup
"""
from docopt import docopt
import devbox.local


def main():
    options = docopt(__doc__, options_first=True)
    found_cmd = False
    for module in dir(devbox):
        if not module.startswith('_'):
            mod = getattr(devbox, module)
            if hasattr(mod, options['<command>']):
                found_cmd = True
                command = getattr(mod, options['<command>'])
                cmd_options = docopt(command.__doc__, argv=options['<args>'])
                command = command(cmd_options)
                command.run()
    if not found_cmd:
        print('Invalid Command, pleae try devbox -h')
