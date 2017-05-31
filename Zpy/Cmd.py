import cmd
import atexit
import subprocess
import readline
import os

from Zpy.Processor import Processor
from Zpy.Completer import Completer
import sys

class Cmd(cmd.Cmd):
    def __init__(self):
        super(Cmd, self).__init__()
        self.prompt = '(Zpy) '

        self.processor = Processor()
        self.completer = Completer()

        self.init_history()
        self.init_env()


    def init_env(self):
        if 'libedit' in readline.__doc__:
            readline.parse_and_bind("bind ^I rl_complete")
        else:
            readline.parse_and_bind("tab: complete")
    def init_history(self):
        histfile = os.path.join(os.getcwd(), ".python_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
            readline.write_history_file(histfile)
        except (FileNotFoundError, PermissionError):
            readline.write_history_file(histfile)
            pass
        atexit.register(readline.write_history_file, histfile)
    def default(self, line):
        print(self.processor.forward(line))

    def do_EOF(self, line):
        print("Bye bye!")
        sys.exit(0)

    def do_help(self, arg):
        readme_location = os.path.join(os.path.dirname(os.path.dirname(__file__)), "README.md")
        print(  open(readme_location).read())
    def cmdloop(self, intro=None):

        while True:
            try:
                super(Cmd, self).cmdloop(intro="")
                self.postloop()
                break
            except KeyboardInterrupt as ex:
                print("^C")
            except Exception as ex:
                print(ex)

    def complete(self, text, index):
        return self.completer.complete(text, index)


if __name__ == "__main__":
    Cmd().complete("ls",0)