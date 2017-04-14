
import subprocess
from prompt_toolkit.completion import Completer
from Zpy.Pipeline import  Pipeline

class Completer(Completer):
    def __init__(self):
        from Zpy.languages.LanguageAnalyzer import LanguageAnalyzer

        self.token = ""
        self.completions = []
        self.lang_analyzer = LanguageAnalyzer()
        self.pipeline = Pipeline()
        pass


    def get_completions(self, document, complete_event):

        #Allow only tap completion
        if not complete_event.completion_requested:
            return ''
        line = document.current_line

        #Complete only last pipeline
        line = self.pipeline.split(line=line)[-1]

        lang = self.lang_analyzer.get_lang_for_complete_line(line)


        return lang.complete(line)

# class Completer(object):
#
#     def __init__(self):
#         self.completer = XonshCompleter()
#         load_builtins()
#
#         self.prefix = ""
#         self.words = []
#         #from xonsh.completers import _aliases
#        # print(_aliases._list_completers(''))
#
#         #bash_completion.bash_completions('git','git', 0,3 )
#
#     def complete(self, text, index):
#         if self.prefix != text:
#             self.prefix = text
#             #print(text)
#             origline = readline.get_line_buffer()
#             line = origline.lstrip()
#             stripped = len(origline) - len(line)
#             begidx = readline.get_begidx() - stripped
#             endidx = readline.get_endidx() - stripped
#             print(self.completer)
#             self.words = self.completer.complete(text, line, begidx, endidx, )[0]
#
#         try:
#             return self.words[:5][index]
#         except IndexError:
#             return None
