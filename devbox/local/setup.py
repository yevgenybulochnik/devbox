from devbox.base_command import BaseCommand
import getpass
import os
import os.path as p
import sys
import pkg_resources
from plumbum import local


class Setup(BaseCommand):
    """
    Usage:
        setup [options] [<username>]

    Options:
        -h, --help
        --gotty
    """
    def home_dir(self, user):
        HOME = p.join(os.sep, 'home', user)
        return HOME

    def setup_gotty(self):
        if self.options['<username>']:
            user = self.options['<username>']
        else:
            user = getpass.getuser()
        gotty_url = 'https://github.com/yudai/gotty/releases/download/v1.0.1/gotty_linux_amd64.tar.gz'
        wget = local['wget']
        tar = local['tar']['-xf']
        mkdir = local['mkdir']
        HOME = self.home_dir(user)
        webterm_path = p.join(HOME, 'webterm')
        zip_file_path = p.join(webterm_path, 'gotty.tar.gz')
        dot_gotty = pkg_resources.resource_filename('devbox', 'config_files/gotty/.gotty')
        if self.options['<username>']:
            if not os.geteuid() == 0:
                sys.exit('\n When using <username> this command must be run as root \n')
            sudo = local['sudo']['-u', user]
            su = local['su']
            cp = local['cp']
            chown = local['chown']
            sudo[mkdir[webterm_path]]()
            sudo[wget[gotty_url, '-O', zip_file_path]]()
            sudo[tar[zip_file_path, '-C', webterm_path]]()
            cp[f'{dot_gotty}', f'{webterm_path}']()
            chown[f'{user}:{user} {webterm_path}/.gotty'.split()]()
            su['-c', 'pm2 start ~/webterm/gotty -- --config ~/webterm/.gotty zsh', '-', f'{user}']()
        else:
            # Need to rewrite the implementation of this, if user runs this command on an already provisioned server
            mkdir[webterm_path]()
            wget[gotty_url, '-O', zip_file_path]()
            tar[zip_file_path, '-C', webterm_path]()
            pm2 = local['pm2']['start ~/webterm/gotty -- zsh'.split()]()

    def run(self):
        if self.options['--gotty']:
            self.setup_gotty()
