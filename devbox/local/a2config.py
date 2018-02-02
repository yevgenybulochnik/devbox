from devbox.base_command import Base_Command
from plumbum import local


class a2config(Base_Command):
    def run(self):
        print(self.options)
