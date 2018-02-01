from devbox.base_command import Base_Command
import subprocess
from plumbum import local


class adduser(Base_Command):
    """Add new user"""
    def run(self):
        print("hello")
        print(self.options)
