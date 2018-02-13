from devbox.base_command import BaseCommand
import getpass
import os
import os.path as p
import sys
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
        if self.options['<username>']:
            if not os.geteuid() == 0:
                sys.exit('\n When using <username> this command must be run as root \n')
            sudo = local['sudo']['-u', user]
            sudo[mkdir[webterm_path]]()
            sudo[wget[gotty_url, '-O', zip_file_path]]()
            sudo[tar[zip_file_path, '-C', webterm_path]]()
        else:
            mkdir[webterm_path]()
            wget[gotty_url, '-O', zip_file_path]()
            tar[zip_file_path, '-C', webterm_path]()

    def run(self):
        if self.options['--gotty']:
            self.setup_gotty()
