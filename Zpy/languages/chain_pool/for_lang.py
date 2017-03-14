from Zpy.languages.Language import Language
#from Zpy.Processor import Processor
import re
import json

class ForLanguage(Language):
    def __init__(self):
        super(ForLanguage, self).__init__()
        self.lang_regex = r"( *?\[.*?for.*?\] )"
        self.lang_regex_compiled = re.compile(self.lang_regex)

    def isLangPrefix(self, line):
        return super().isLangPrefix(line)

    def complete(self, line):
        return ""

    def prepare(self,line):
        """
        Remove `j` character at begin
        :param line: line to preparing
        :return: striped line without j-symbol at begining
        >>> prepare = ForLanguage().prepare
        >>> prepare(" [ for ] j [1,2,3,4].map( function(e) { return e*2 } )")
        'j [1,2,3,4].map( function(e) { return e*2 } )'
        >>> prepare("[for]     some string")
        'some string'

        """
        return re.sub(self.lang_regex,"",line,1).strip()



    def isLang(self, line):
        """
        JS language contain upper case letter `j` at begin, like '   j [1,2,3,4].map( function(e) { return e*2 } )'
        :param line: command
        :return: True if this is js syntax False otherwise

        >>> isLang = ForLanguage().isLang
        >>> isLang("[for] j  2 + 3 * 4")
        True
        >>> isLang("[for ] j  2 + 3 * 4")
        True
        >>> isLang("j 8 + 5")
        False
        """
        return self.lang_regex_compiled.match(line) is not None

    def evaluate(self, line, processor=None, stdin=""):
        """

        :param line:
        :param processor:
        :param stdin:
        :return:
        >>> evaluate = ForLanguage().evaluate
        >>> proc = Processor()
        >>> evaluate("for j z + 4",proc,[2,3,4])
        [6, 7, 8]
        >>> evaluate("for j z + 'asd'",proc,['a','b',3])
        ['aasd', 'basd', '3asd']
        """
        line = self.prepare(line)

        if stdin is None or len(stdin) == 0:
            raise Exception("No stdin passed into FOR language")
        if processor == None:
            raise Exception("No processor passed into evaluate method")


        iter_stdin = stdin

        # Check is Iterable
        #EEROOR STRING IS ITERABLE
        """
        iterable = True
        try:
            iterator = iter(stdin)
        except TypeError:
            # not iterable
            iterable = False
        """

        iterable = isinstance(stdin,list) or isinstance(stdin, tuple)
        # Split or add new dimension if is not iterable
        if not iterable:
            if isinstance(stdin,str):
                iter_stdin = stdin.split("\n")
            else:
                iter_stdin = [stdin]

        result = []

        for stdin_obj in iter_stdin:
            result.append(processor.forward(line, stdin=stdin_obj))

        return result




