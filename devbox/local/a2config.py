from devbox.base_command import Base_Command
import sys
import os
import os.path as p
from plumbum import local


class a2config(Base_Command):

    def check_install(self):
        install_apache = local['apt']['install -y apache2'.split()]
        a2_exists = '/etc/apache2'
        if not p.isdir(a2_exists):
            install_apache()
            self.enable_mods()

    def enable_mods(self):
        mods = [
            'proxy',
            'proxy_http',
            'proxy_wstunnel',
            'rewrite',
            'ssl'
        ]
        a2enmod = local['a2enmod']
        for mod in mods:
            a2enmod(mod)

    def run(self):
        if not os.geteuid() == 0:
            sys.exit('\n This command must be run as Root \n')
        self.check_install()
