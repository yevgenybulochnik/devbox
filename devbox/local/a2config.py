from devbox.base_command import Base_Command
import sys
import os
from plumbum import local


class a2config(Base_Command):
    def run(self):
        if not os.geteuid() == 0:
            sys.exit('\n This command must be run as Root \n')
        print(self.options)
