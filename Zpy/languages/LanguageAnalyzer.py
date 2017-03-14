from Zpy.languages.python.python_lang import PythonLanguage
from Zpy.languages.shell.unix_lang import UnixLang
from Zpy.languages.js.js_lang import JavascriptLanguage
from Zpy.languages.chain_pool.for_lang import ForLanguage
class LanguageAnalyzer():
    def __init__(self):
        self.languages = [JavascriptLanguage(),UnixLang(),ForLanguage(), PythonLanguage()]

    def get_lang_for_complete_line(self, line_):
        """
        Analyze current line and returns language which will complete this line
        :param line_: some command
        :return: Language which will complete this line
        >>> analize = LanguageAnalyzer().get_lang_for_complete_line
        >>> analize('`git').__class__.__name__
        'UnixLang'
        """
        line = line_.strip()
        selected_langs = list(filter(lambda lang: lang.isLangPrefix(line), self.languages))

        if len(selected_langs) == 0:
            raise Exception("Cannot find language for completion this line %s" % line)

        if len(selected_langs) > 1:
            raise Exception("Find more than one langs(%s) for comletion this line %s" % (selected_langs.join(","), line))

        #print("FINDED LANG", selected_langs[0])
        return selected_langs[0]
    def analize(self, line):
        """
        Analyze current command and returns language
        :param line: some command
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
        >>> analize(' j  2 + 3').__class__.__name__
        'JavascriptLanguage'
        >>> analize('[for] a').__class__.__name__
        'ForLanguage'
        """
        comm = line.strip()

        selected_langs = list( filter(lambda lang : lang.isLang(comm), self.languages))
        if len(selected_langs) == 0:
            raise Exception("Cannot find language for evaluate this command %s" % comm)

        if len(selected_langs) > 1:
            raise Exception("Find more than one langs(%s) for this command %s" % (selected_langs.join(","), comm))

        return selected_langs[0]

