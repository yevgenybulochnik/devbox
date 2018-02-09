from devbox.base_command import Base_Command
import sys
import os
import os.path as p
from plumbum import local
import pkg_resources
from string import Template


class a2config(Base_Command):
    """
    Usage:
        a2config --domain=DOMAIN --authuser=USER --password=PASSWORD

    Options:
        -d, --domain=DOMAIN
        -u, --authuser=USER
        -p, --password=PASSWORD
    """
    def check_install(self):
        install_apache = local['apt']['install -y apache2'.split()]
        a2_exists = '/etc/apache2'
        if not p.isdir(a2_exists):
            install_apache()
            self.enable_mods()
            disable_default_site = local['a2dissite']['000-default.conf']()

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

    def create_ssl_cert(self):
        cert_dir = '/etc/apache2/ssl'
        os.makedirs(cert_dir, exist_ok=True)
        create_cert = local['openssl']
        arguments = f'req -x509 -nodes -days 365 -newkey rsa:2048 -keyout {cert_dir}/apache.key -out {cert_dir}/apache.crt -subj /C=US/ST=OR/L=Portland/O=""/OU=""/CN=""'.split()
        create_cert(arguments)

    def create_password(self):
        password_file = '/etc/apache2/.htpasswd'
        username = self.options['--authuser']
        password = self.options['--password']
        if not p.isfile(password_file):
            open(password_file, 'w').close()
        htpasswd = local['htpasswd'][f'-b {password_file} {username} {password}'.split()]
        htpasswd()

    def create_virtual_hosts(self):
        vh_templates = os.listdir(pkg_resources.resource_filename('devbox', 'config_files/a2'))
        server_name = self.options['--domain']
        enable_site = local['a2ensite']
        for vh_template in vh_templates:
            resource = pkg_resources.resource_filename('devbox', f'config_files/a2/{vh_template}')
            temp = Template(open(resource).read())
            vh = temp.substitute({'DOMAIN': server_name})
            if vh_template == 'static':
                with open(f'/etc/apache2/sites-available/{server_name}.conf', 'w') as conf:
                    conf.write(vh)
                os.makedirs(f'/var/www/{server_name}', exist_ok=True)
                enable_site(f'{server_name}.conf')
            else:
                with open(f'/etc/apache2/sites-available/{vh_template}.{server_name}.conf', 'w') as conf:
                    conf.write(vh)
                enable_site(f'{vh_template}.{server_name}.conf')
        restart_apache = local['service']['apache2 restart'.split()]()

    def run(self):
        if not os.geteuid() == 0:
            sys.exit('\n This command must be run as Root \n')
        self.check_install()
        self.create_ssl_cert()
        self.create_password()
        self.create_virtual_hosts()
