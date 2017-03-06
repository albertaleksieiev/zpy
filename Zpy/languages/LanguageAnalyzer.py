from Zpy.languages.python.python_lang import PythonLanguage
from Zpy.languages.shell.unix_lang import UnixLang


class LanguageAnalyzer():
    def __init__(self):
        self.languages = [UnixLang(), PythonLanguage()]
    def analize(self, command):
        """
        Analyze language
        :param command: some command
        :return: language which have this syntax
        >>> analize = LanguageAnalyzer().analize
        >>> from Zpy.Utils import get_linux_commands
        >>> unix_commands = get_linux_commands()
        >>> analize('pwd').__class__.__name__
        'UnixLang'
        >>> list(filter(lambda  x : "UnixLang" != x, [analize(x).__class__.__name__ for x in unix_commands]))
        []
        >>> analize('`git').__class__.__name__
        'UnixLang'
        >>> analize('git').__class__.__name__
        'PythonLanguage'
        >>> analize('[i for i in range(11)').__class__.__name__
        'PythonLanguage'
        """
        comm = command.strip()

        selected_langs = list( filter(lambda lang : lang.isLang(comm), self.languages))
        if len(selected_langs) == 0:
            raise Exception("Cannot find language for evaluate this command %s" % comm)

        if len(selected_langs) > 1:
            raise Exception("Find more than one langs(%s) for this command %s" % (selected_langs.join(","), comm))

        return selected_langs[0]

