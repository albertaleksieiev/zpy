import os,subprocess
import traceback
from Zpy.Pipeline import Pipeline
from Zpy.languages.LanguageAnalyzer import LanguageAnalyzer
class Processor():
    def __init__(self):
        self.pipeline = Pipeline()
        self.language_analyzer = LanguageAnalyzer()
        self.last_zcommand = ""


        self.info = {
            'pipes_count' : 0
        }



    def forward(self, line, stdin =""):
        """
        Evaluate command by some language interpreter
        :param line: line command
        :param stdin: stdin value
        :return: result of execution (for unix command we dont return nothing if lenght of pipe items = 1)
        >>> import tempfile, os
        >>> tempdir = tempfile.gettempdir()
        >>> tmpfile = os.path.join(tempdir,'zpy_test.txt')
        >>> proc = Processor()
        >>> forward = proc.forward
        >>> len(forward("['.', '..'] |[for] ls $z"))
        2
        >>> forward('"asd" |[for] z')
        ['asd']
        >>> forward('j [2,3,4,5] |[for] j z + 15')
        [17, 18, 19, 20]
        >>> forward("~import os, re")
        ''
        >>> forward("'123'*3")
        '123123123'
        >>> forward("[i + 1 for i in range(10)]")
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        >>> forward("echo 'asd' | z")
        'asd'
        >>> forward("echo 'some_data' | (z.strip() + 'data') | cat > %s" % tmpfile )
        ''
        >>> forward("cat %s | z" % tmpfile)
        'some_datadata'
        >>> forward("cd %s" % tempdir.strip())
        ''
        >>> forward("pwd | True if len(os.listdir(z.strip())) > 0 else False ")
        True
        """
        #>>> forward('"https://www.reddit.com/r/books/" | `wget -qO- $z |  re.findall(r"Book[^\.].*?",z,re.IGNORECASE) | True if len(z) > 0 else False')
        #True



        if len(line) == 0:
            return

        commands = self.pipeline.split(line=line)
        self.info['pipes_count'] = len(commands)
        for command in commands:
            lang = self.language_analyzer.analize(command)
            try:
                stdin = lang.evaluate(command.strip(), self, stdin=stdin)
            except SyntaxError as e:
                print("Cannot evaluate line `%s`" % command.strip())
                print(e)
            except Exception as e:
                traceback.print_exc()
        if (isinstance(stdin, str) and stdin == "") or stdin is None:
            pass
        else:
            if isinstance(stdin,str):
                stdin = stdin.strip()
        self.last_zcommand = line

        return stdin
