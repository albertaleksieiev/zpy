import subprocess

from prompt_toolkit.completion import Completion



class UnixCompleter:
    def __init__(self):
        self.last_command = {
            "command": "",
            "command_arguments" : ""
        }
        self.completions = []

    def get_unix_completions(self, line):
        """
        Get unix complete by using `compgen`
        :param line:
        :return: array of completions
        >>> completer = UnixCompleter()
        >>> "ls" in completer.get_unix_completions('l')
        True
        >>> len(completer.get_unix_completions('pnoqincoqnaoszni2oindo1noozincoinscmzmcnzxx1211'))
        0

        """
        proc = subprocess.Popen(['compgen -c %s' % line], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        return proc.communicate()[0].decode().strip().split('\n')

    def complete(self, line):
        """
        :param line: Complete line
        :return: generator of completion
        >>> completer = UnixCompleter()
        >>> "ls" in [i.text for i in list(completer.complete('l'))]
        True
        >>> "-l" in [i.text for i in list(completer.complete('ls -l'))]
        True
        """
        #print('line', line)
        commands = line.strip().split(' ')
        #print('commands',commands)
        if len(commands) == 1:
            # Command without arguments
            command = commands[0]


            # Check this command was be already using in search(looking in cache)

            if not line.startswith(self.last_command['command']) or len(self.last_command['command']) == 0:
                self.last_command = {
                    "command": command,
                    "command_arguments" : ""
                }
                self.completions = self.get_unix_completions(line)

            for completion in self.completions:
                yield Completion(completion, start_position=0)
        else:
            # Check for arguments

            arguments = commands[1:]
            arguments_joined = " ".join(arguments)

            if not arguments_joined.startswith(self.last_command["command_arguments"]) or len(self.last_command['command_arguments']) == 0:
                self.last_command["command_arguments"] = arguments_joined



            yield Completion( " ".join(arguments) , start_position=0)