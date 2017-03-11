from __future__ import unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory

from pygments.lexers.python import Python3Lexer as PythonLexer

import Zpy.frontend.messages as frontend_message
from Zpy.frontend.DocumentStyle import DocumentStyle
from Zpy.Processor import Processor
from Zpy.Completer import Completer








class Cmd:
    def __init__(self):
        self.prompt = '(Zpy) '

        self.processor = Processor()
        self.completer = Completer()
    def cmdloop(self):
        history = FileHistory(".history")

        print(frontend_message.get_welcome_message())
        while True:
            try:
                while True:
                    text = prompt(self.prompt, lexer=PythonLexer,
                                  completer=self.completer,
                                  style=DocumentStyle, history=history)
                    self.processor.forward(text)
            except KeyboardInterrupt as ex:
                print("^C")
            except EOFError:
                print(frontend_message.get_bye_message())
                break
            except Exception as ex:
                print(ex)


