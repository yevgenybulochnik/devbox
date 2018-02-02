"""
Devbox is a python command line application that assists in provisioning a development server.

Usage:
    devbox adduser <username> [--dotfiles=URL]
    devbox a2config

Options:
    -h --help
    -d URL, --dotfiles=URL

"""
from docopt import docopt
import devbox.local


def main():
    options = docopt(__doc__)
    for module in dir(devbox):
        if not module.startswith('_'):
            mod = getattr(devbox, module)
            for k, v in options.items():
                if hasattr(mod, k) and v:
                    command = getattr(mod, k)
                    command = command(options)
                    command.run()
