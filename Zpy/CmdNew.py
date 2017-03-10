from __future__ import unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory

from pygments.lexers.python import PythonLexer as PythonLexer
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle

from Zpy.Processor import Processor
from Zpy.Completer import Completer





class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProgressBar: 'bg:#00aaaa'
    }
    styles.update(DefaultStyle.styles)

class Cmd:
    def __init__(self):
        self.prompt = '(Zpy) '

        self.processor = Processor()
        self.completer = Completer()
    def cmdloop(self):
        history = InMemoryHistory()


        while True:
            text = prompt(self.prompt, lexer=PythonLexer,
                          completer=self.completer,
                          style=DocumentStyle, history=history)
            self.processor.forward(text)

