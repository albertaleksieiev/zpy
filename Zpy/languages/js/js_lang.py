import os
import re

from Zpy.languages.Language import Language
from libs import execjs

class JavascriptLanguage(Language):
    def __init__(self):
        super(JavascriptLanguage, self).__init__()
        self.lang_regex = r"( *?j )"
        self.lang_regex_compiled = re.compile( self.lang_regex)

    def prepare(self,line):
        """
        Remove `j` character at begin
        :param line: line to preparing
        :return: striped line without j-symbol at begining
        >>> prepare = JavascriptLanguage().prepare
        >>> prepare("   j [1,2,3,4].map( function(e) { return e*2 } )")
        '[1,2,3,4].map( function(e) { return e*2 } )'
        >>> prepare("j     some string")
        'some string'

        """
        return re.sub(self.lang_regex,"",line).strip()
    def isLangPrefix(self, line):
        return self.isLang(line)

    def isLang(self, line):
        """
        JS language contain upper case letter `j` at begin, like '   j [1,2,3,4].map( function(e) { return e*2 } )'
        :param line: command
        :return: True if this is js syntax False otherwise

        >>> isLang = JavascriptLanguage().isLang
        >>> isLang("  j  2 + 3 * 4")
        True
        >>> isLang(" 8 + 5")
        False
        """
        return self.lang_regex_compiled.match(line) is not None


    def complete(self, line):
        return super().complete(line)

    def evaluate(self, line, processor=None, stdin=""):
        """
        Evaluate js code
        :param line: line for evaluation
         param processor: Zpy processor
        :param stdin: stdin will be passed to lang as Z variable
        :return: evaluation results
        >>> eval = JavascriptLanguage().evaluate
        >>> eval('j 2 + 3')
        5
        """
        return execjs.eval(self.prepare(line))
