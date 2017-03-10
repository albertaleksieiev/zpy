class Language:

    def isLang(self, line):
        """
        This language know about this line, cause it will be evaluated by using this lang class,
            method evaluation(line).
        :param line: line from current language
        :return: True if it knows else False
        """
        return False  # we dont know this line

    def isLangPrefix(self, line):
        """
        Do the same as isLang method, except evaluation. This lang will be evaluated for completion
        :param line: command
        :return: True if this lang
        """
        return False

    def complete(self, line):
        """
        Complete this line
        :param line: line for completion
        :return: generator of completions
        """

    def evaluate(self, line):
        """
        Evaluate this line
        :param line: command line for evaluation
        :return: object, or decoded string, this object will be sended to the next chain as stdin
        """
        return ""

    def complete(self, text, state):
        """
        Trying complete this line
        :param text: Text to complete
        :param state:
        :return: array with complete results
        """
        return []
