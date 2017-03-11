from prompt_toolkit.completion import Completion

class PythonCompleter():
    def __init__(self):
        self.last_command = {
            "command": "",
            "command_arguments" : ""
        }
        self.completions = []

        # List of completions
        # Taken from `xonsh` and `pygments` modules
        completion_1 = ('__import__', 'import', 'abs', 'all', 'any', 'bin', 'bool', 'bytearray', 'bytes',
             'chr', 'classmethod', 'cmp', 'compile', 'complex', 'delattr', 'dict',
             'dir', 'divmod', 'enumerate', 'eval', 'filter', 'float', 'format',
             'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id',
             'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list',
             'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct',
             'open', 'ord', 'pow', 'print', 'property', 'range', 'repr', 'reversed',
             'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str',
             'sum', 'super', 'tuple', 'type', 'vars', 'zip')
        completion_2 = ('__import__', 'abs', 'all', 'any', 'apply', 'basestring', 'bin',
             'bool', 'buffer', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod',
             'cmp', 'coerce', 'compile', 'complex', 'delattr', 'dict', 'dir', 'divmod',
             'enumerate', 'eval', 'execfile', 'exit', 'file', 'filter', 'float',
             'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'hex', 'id',
             'input', 'int', 'intern', 'isinstance', 'issubclass', 'iter', 'len',
             'list', 'locals', 'long', 'map', 'max', 'min', 'next', 'object',
             'oct', 'open', 'ord', 'pow', 'property', 'range', 'raw_input', 'reduce',
             'reload', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice',
             'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type',
             'unichr', 'unicode', 'vars', 'xrange', 'zip')
        completion_3 = ('assert', 'break', 'continue', 'del', 'elif', 'else', 'except',
             'exec', 'finally', 'for', 'global', 'if', 'lambda', 'pass',
             'print', 'raise', 'return', 'try', 'while', 'yield',
             'yield from', 'as', 'with', 'from')
        completion_4 = ('and', 'else', 'for', 'if', 'in', 'is', 'lambda', 'not', 'or',
            '+', '-', '/', '//', '%', '**', '|', '&', '~', '^', '>>', '<<', '<',
            '<=', '>', '>=', '==', '!=', ',', '?', '??')
        completion_5 = ('as', 'assert', 'break', 'class', 'continue', 'def', 'del',
            'elif', 'except', 'finally:', 'from', 'global', 'import',
            'nonlocal', 'pass', 'raise', 'return', 'try:', 'while', 'with',
            'yield ', '-', '/', '//', '%', '**', '|', '&', '~', '^', '>>', '<<',
            '<', '<=', '->', '=', '+=', '-=', '*=', '/=', '%=', '**=',
            '>>=', '<<=', '&=', '^=', '|=', '//=', ';', ':', '..')
        self.command_list = set(completion_1) | set(completion_2) | set(completion_3) | set(completion_4) | set(completion_5)

    def get_python_completion(self, line):
        """
        Get completion for python
        :param line: line for completions
        :return: list of completions or empty list
        """

        return list(filter(lambda x : x.startswith(line), self.command_list))



    def complete(self, line):
        """
        :param line: Complete line
        :return: generator of completion
        >>> completer = PythonCompleter()
        >>> "with" in [i.text for i in list(completer.complete('with'))]
        True
        >>> "import" in [i.text for i in list(completer.complete('import'))]
        True
        >>> "somecommm" in [i.text for i in list(completer.complete('import'))]
        False
        >>> [i.text for i in list(completer.complete('for im'))]
        ['import']
        """

        if len(line) > 0 and line[-1] == " ":
            #End of command, do not complete
            return

        commands = line.strip().split(' ')
        if len(commands) == 1:
            # Command without arguments
            command = commands[0]

            # Check this command was be already using in search(looking in cache)
            if not line.startswith(self.last_command['command']) or len(self.last_command['command']) == 0:
                self.last_command = {
                    "command": command,
                    "command_arguments": ""
                }
                self.completions = self.get_python_completion(line)

            for completion in filter(lambda x: x.startswith(line), self.completions):
                yield Completion(completion, start_position=-len(line))
        else:
            # Check for arguments
            arguments = commands[1:]
            arguments_joined = " ".join(arguments)

            if not arguments_joined.startswith(self.last_command["command_arguments"]) or len(
                    self.last_command['command_arguments']) == 0:
                self.last_command["command_arguments"] = arguments_joined


            #Recursion
            completions = self.complete(arguments[-1])

            for completion in completions:
                yield Completion(completion.text, start_position=-len(arguments[-1]))