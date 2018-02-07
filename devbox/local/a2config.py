from devbox.base_command import Base_Command
import sys
import os
import os.path as p
from plumbum import local
import pkg_resources
from string import Template


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

    def create_virtual_hosts(self):
        vhs = [
            'jupyter',
            'preview',
            'static',
            'webterm'
        ]
        server_name = self.options['--domain']
        for vh_template in vhs:
            resource = pkg_resources.resource_filename('devbox', f'config_files/a2/{vh_template}')
            temp = Template(open(resource).read())
            vh = temp.substitute({'DOMAIN': server_name})
            if vh_template == 'static':
                conf = open(f'/etc/apache2/sites-available/{server_name}.conf', 'w')
                conf.write(vh)
                conf.close()
            else:
                conf = open(f'/etc/apache2/sites-available/{vh_template}.{server_name}.conf', 'w')
                conf.write(vh)
                conf.close()

    def run(self):
        if not os.geteuid() == 0:
            sys.exit('\n This command must be run as Root \n')
        self.check_install()
        self.create_virtual_hosts()
