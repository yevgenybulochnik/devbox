"""
Devbox is a python command line application that assists in provisioning a development server.

Usage:
    devbox

Options:
    -h --help
"""
from docopt import docopt

def main():
    arguments = docopt(__doc__)
