import cmd
import atexit
import os
import readline

from ZPy.Processor import Processor
class Cmd(cmd.Cmd):
    def __init__(self):
        super(Cmd, self).__init__()

        self.prompt = '(Zpy) '
        self.processor = Processor()
        self.init_history()

    def init_history(self):
        histfile = os.path.join(os.getcwd(), ".python_history")
        try:
            readline.read_history_file(histfile)
            readline.set_history_length(1000)
            readline.write_history_file(histfile)
        except FileNotFoundError:
            readline.write_history_file(histfile)
            pass
        atexit.register(readline.write_history_file, histfile)
    def default(self, line):
        self.processor.forward(line)
    def do_EOF(self, line):
        print("Bye bye!")
        exit(0)
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

    def completedefault(text, line, begidx, endidx):
        print('complete')
        return []
    def do_fuck(self):
        pass



