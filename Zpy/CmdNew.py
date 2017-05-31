from __future__ import unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from pygments.lexers.python import Python3Lexer as PythonLexer

import Zpy.frontend.messages as frontend_message
from Zpy.frontend.DocumentStyle import DocumentStyle
from Zpy.Processor import Processor
from Zpy.Completer import Completer

import os



class Cmd:
    def __init__(self):
        self.prompt = '(Zpy) '

        self.processor = Processor()
        self.completer = Completer()

    def process_file(self, location):
        if not os.path.exists(location):
            return "File not exist!"

        with open(location) as f:
            content = f.readlines()

        return self.processor.forward(" ".join(list(filter(lambda x: not x.startswith("#"), content))) )
    def cmdloop(self):

        history_location = os.path.join(os.path.dirname(os.path.abspath(__file__)),".history")
        history = FileHistory(history_location)

        print(frontend_message.get_welcome_message())
        while True:
            try:
                while True:
                    text = prompt(self.prompt, lexer=PythonLexer,
                                  completer=self.completer,
                                  style=DocumentStyle, history=history)
                    res = self.processor.forward(text)

                    if(isinstance(res, str)):
                        res = res.strip()
                        if(len(res)>0):
                            print(res)
                    elif res is not None:
                        print(res)


            except KeyboardInterrupt as ex:
                print("^C")
            except EOFError:
                print(frontend_message.get_bye_message())
                break
            except Exception as ex:
                print(ex)


