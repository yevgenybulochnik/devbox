from devbox.base_command import Base_Command
import subprocess
import sys
import os
import os.path as p
from plumbum import local


class Devbox_User(object):

    def __init__(self, username, password, dotfiles_url):
        self.username = username
        self.password = password
        self.dotfiles_url = dotfiles_url
        self.HOME = f'/home/{self.username}'

    def create(self):
        adduser = local['adduser'][f'--disabled-password --gecos "" {self.username}'.split()]
        return adduser()

    def set_pwdls_sudo(self):
        file = open(f'/etc/sudoers.d/{self.username}', 'w')
        file.write(f'{self.username} ALL=(ALL) NOPASSWD:ALL')
        file.close()

    def get_dotfiles(self):
        if self.dotfiles_url:
            sudo = local['sudo'][f'-u {self.username}'.split()]
            git = local['git'][f'clone {self.dotfiles_url} {self.HOME}/dotfiles'.split()]
            return sudo[git]()

    def install_file_exists(self):
        install_exists = f'{self.HOME}/dotfiles/install.sh'
        if p.isfile(install_exists):
            return True
        return False

    def install_dotfiles(self):
        su = local['su'][f'-c {self.HOME}/dotfiles/install.sh - {self.username}'.split()]
        return su()


class adduser(Base_Command):
    """Add new user"""
    def run(self):
        if not os.geteuid() == 0:
            sys.exit('\n This command must be run as Root \n')
        new_user = Devbox_User(
            self.options['<username>'],
            self.options['<password>'],
            self.options['--dotfiles']
        )
        new_user.create()
        new_user.set_pwdls_sudo()
        new_user.get_dotfiles()
        if new_user.install_file_exists():
            new_user.install_dotfiles()
