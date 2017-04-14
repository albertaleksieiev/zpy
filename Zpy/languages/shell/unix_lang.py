import subprocess, os, re
from Zpy.Utils import get_linux_commands
from Zpy.storage.SuffixTree import SuffixTree
from Zpy.languages.Language import Language
from Zpy.languages.shell.unix_completer import UnixCompleter
import json

class WrondDstDirException(Exception): pass


class UnixLang(Language):
    def __init__(self):
        super(UnixLang, self).__init__()
        self.buildTree()
        self.current_dir = os.getcwd()
        self.unix_completer = UnixCompleter()

    def buildTree(self):
        """
        Build suffix tree for fast search
        :return:
        """
        commands = get_linux_commands()
        #Add leaf data column
        self.Tree = SuffixTree([{"word": x, "leaf_data": True} for x in commands])

    def isLang(self, line):
        """
        Check if line is shell command
        :param line: command
        :return: True if is shell else False
        >>> UnixLang().isLang("`vim")
        True
        >>> UnixLang().isLang("ls")
        True
        >>> UnixLang().isLang("2+3")
        False
        """
        return (len(line) > 0 and line[0]=="`") or self.Tree.find(line)
    def isLangPrefix(self, line):
        """
        Do the same as isLang method, except evaluation. This lang will be evaluated for completion
        :param line: command
        :return: True if this lang
        """
        return self.isLang(line)

    def complete(self, line):
        """
        Complete this line
        :param line: line for completion
        :return: generator of completions
        >>> completer = UnixLang()
        >>> "ls" in [i.text for i in list(completer.complete('l'))]
        True
        """

        return self.unix_completer.complete(self.prepare(line))

    def prepare(self,line):
        """
        Prepare line to execution.
        Remove ` character from line if their present in line and position of character is first.
        :param line: line to prepare
        :return: prepared line to execution
        >>> UnixLang().prepare("`ls")
        'ls'
        >>> UnixLang().prepare("````````````````````````````pwd")
        'pwd'
        >>> UnixLang().prepare("ls")
        'ls'
        >>> UnixLang().prepare([i for i in range(10)])
        '[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]'
        """
        if len(line) > 0 and line[0]=="`":
            return self.prepare(line[1:])
        return str(line)

    def set_directory(self, dir):
        """
        Change current directory
        :param dir: new directory
        :return: True if success else raise WrondDstDirException
        >>> import os,tempfile
        >>> ul = UnixLang()
        >>> tmpdir = tempfile.gettempdir()
        >>> newdir = os.path.join(tmpdir,"some/cool/dir/yeah")
        >>> os.makedirs(newdir,exist_ok=True)
        >>> ul.set_directory(newdir)
        >>> os.getcwd()[-len("some/cool/dir/yeah"):]
        'some/cool/dir/yeah'
        >>> ul.evaluate('cd ..')
        ''
        >>> ul.evaluate('ls',return_result_anyway=True).strip()
        'yeah'
        >>> ul.evaluate('cd ../../../some')
        ''
        >>> ul.evaluate('ls',return_result_anyway=True).strip()
        'cool'
        """

        ## Expand ~
        expanded_path = os.path.expanduser(dir)
        ##Join
        joined_path = os.path.join(self.current_dir, expanded_path)

        if os.path.isdir(joined_path):
            os.chdir(joined_path)
            self.current_dir = joined_path
        else:
            raise WrondDstDirException("%s is not directory!" % dir)

    def create_proc(self,line, env = None, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=None):
        """
        Create subprocess Popen
        https://docs.python.org/3/library/subprocess.html
        :param line: line to evaluate
        :param env: Env variable
        :param stdin: stdin type
        :param stdout: stdout type
        :param stderr: stderr type
        read more about types
        https://docs.python.org/3/library/subprocess.html#subprocess.DEVNULL
        :return: Popen

        >>> UnixLang().create_proc('echo "DEVNULL|PIPE|STDOUT"', stdout=subprocess.PIPE).communicate()[0].decode().strip()
        'DEVNULL|PIPE|STDOUT'
        """
        proc = subprocess.Popen([line],
                                stdin=stdin,
                                stdout=stdout,
                                stderr=stderr,
                                shell=True,
                                env=env,
                                cwd=self.current_dir)
        return proc

    def eval(self, line, processor = None, env = None, input="", return_result_anyway = False):
        """
        Helping function for evaluation
        """

        if processor is not None and processor.info['pipes_count']  == 1:
            subprocess.check_call([line], shell=True, env=env)
            return ""
        elif return_result_anyway or (processor is not None and processor.info['pipes_count'] > 1):
            proc = self.create_proc(line ,env, stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        else:
            subprocess.check_call([line], shell=True,env=env)
            return ""




        out = proc.communicate(str(input).encode())
        if len(out) == 0:
            return ""
        try:
            return out[0].decode()
        except Exception as ex:
            return str(out[0])[2:-1]

    def evaluate(self, line, processor = None, stdin ="", return_result_anyway = True):
        """
        Evaluate shell command
        :param line: line to execute
        :param processor: Processor instance
        :param stdin: stdin will be passed to stdin PIPE
        :param return_result_anyway: by default if pipes count = 1, result not will be returned, command will be executed and result will be passed to stdout
        :return: result of evaluation, if processor.info['pipes_count'] = 1, nothing will be returned

        >>> UnixLang().evaluate("echo 'xyz\\ncde\\n123' | sort -n",return_result_anyway=True).strip().split('\\n')
        ['cde', 'xyz', '123']
        >>> UnixLang().evaluate("echo 'xyz\\ncde\\n123' | cat -",return_result_anyway=True).strip().split('\\n')
        ['xyz', 'cde', '123']
        >>> os.path.isdir(UnixLang().evaluate("pwd").strip())
        True

        """
        line = self.prepare(line)
        if isinstance(stdin, list) or isinstance(stdin, tuple):
            #Try convert each item to str
            try:
                tmp_stdin = []
                for item in stdin:
                    tmp_stdin.append(str(item))
                stdin = "\n".join(tmp_stdin)
            except:
                stdin = json.dumps(stdin)

        elif not isinstance(stdin, str):
            stdin = json.dumps(stdin)

        env = os.environ.copy()
        env['z'] = stdin

        #is change dir
        match = re.match(r'cd(?:\s+|$)(.*)', line)
        if match:
            dirs = match.groups()
            # Default to cd is home directory
            if len(dirs) == 0 or len(dirs[0]) == 0:
                self.set_directory(os.environ['HOME'])
            else:
                dir = dirs[0]
                if dir == '..':
                    head, tail = os.path.split(self.current_dir)
                    self.set_directory(head)
                else:
                    self.set_directory(dir)
            return ""


        return self.eval(line, processor, env, stdin, return_result_anyway=return_result_anyway)






