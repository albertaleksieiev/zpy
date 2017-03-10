import inspect

from Zpy.languages.shell.unix_lang import UnixLang
from Zpy.languages.Language import Language
from Zpy.modules.module_manager import ModuleManager
from Zpy.modules.zpy import zpy

from prompt_toolkit.completion import Completion

class PythonLanguage(Language):
    def __init__(self):
        super(PythonLanguage, self).__init__()

        self.UnixLang = UnixLang()
        self.exec_command = []
        self.module_manager = ModuleManager()
        self.zpy = zpy(processor=None)

    def isLang(self, line):
        #If not unix :)
        """
        :param line: command
        :return: its python command
        >>> PythonLanguage().isLang("ls")
        False
        >>> PythonLanguage().isLang("2 * 3")
        True

        """
        return not self.UnixLang.isLang(line)
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
        """
        yield Completion(line+'asd', start_position=0)

    def get_module(self, processor):
        if processor is None:
            return {}
        return self.module_manager.get_modules(processor=processor)

    # TODO OPTIMIZE
    def evaluate(self, line, processor=None, stdin=""):
        """
        Evaluate python
        :param line: python line
        :param processor: zpy-processor
        :param stdin: stdin wiil be passed in variable `z`
        :return: result of evaluation

        >>> pl = PythonLanguage()
        >>> pl.evaluate(" 2 + 3 + 7 + 8")
        20
        >>> pl.evaluate("ls")
        NameError("name 'ls' is not defined",)
        >>> pl.evaluate("z['x'] * 15", stdin={'x':15})
        225
        >>> pl.evaluate("~import os, uuid")
        ''
        >>> pl.evaluate("len(str(uuid.uuid4()))")
        36
        """
        if len(line) > 0 and line[0] == "~":
            self.exec_command.append(line[1:])
            return ""

        # Add default imports
        default_imports = self.zpy.get_def_imports_dict()
        for name, imp in default_imports.items():
            if imp not in self.exec_command:
                self.exec_command.append(imp)

        exec("\n".join(self.exec_command) + "\n")

        # Set z-variable
        z = stdin
        # Set modules
        for name, module in self.get_module(processor).items():
            locals()[name.split(".")[-1]] = module

        try:
            res = eval(line)
            is_func = inspect.isfunction(res) or inspect.ismethod(res)
            if is_func and 'zpy_input' in inspect.getargspec(res).args:
                return res(zpy_input=stdin)

            elif is_func or inspect.isroutine(res):
                return res(stdin)
            return res
        except Exception as ex:
            return ex

