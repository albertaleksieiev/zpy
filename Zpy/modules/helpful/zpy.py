
from Zpy.modules.helpful.z import z_base
class zpy(z_base):
    #Constants
    SCRIPTS = "SCRIPTS_PY"
    MODULE = "MODULE_PY"
    DEFAULT_IMPORTS = "DEFAULT_IMPORTS_PY"
    def __init__(self, processor):
        super().__init__(processor)

    """
    Scripts
    """
    def get_scripts(self):
        return self.get_section(section=self.SCRIPTS)

    def script(self,name):
        script_section = self.get_script_section_and_config()['section']
        return script_section[name]

    def add_script(self, name):
        def wrap(zpy_input):
            return self.add_new_script(name=name, script=zpy_input)
        return wrap

    def remove_script(self, name):
        return self.remove_from_section(self.SCRIPTS,name)

    def add_new_script(self, name, script):
        return self.add_to_section(self.SCRIPTS, name, value=script)

    """
        Utils
    """
    def as_table(self, line):
        """
        :param line: Convert data which splited by '\n' or array into beautiful table splited by '\n'
        :return: beautified table
        >>> len(zpy(processor=None).as_table([[0, 1, 4, 9, 16], [25, 36, 49, 64, 81]])) > 0
        True
        """
        from terminaltables import AsciiTable, SingleTable
        if isinstance(line, str):
            arr = line.split('\n')
            prepared_arr = [' '.join(x.split()).split(' ') for x in arr]
        else: #Iterable
            prepared_arr = line



        ##Todo refactor
        #prepared_arr = [' '.join(x.split() if isinstance(x,str) else str(x)).split(' ') for x in arr]
        return SingleTable(prepared_arr).table

    """
        Evaluation
    """
    def eval(self, name, input=""):
        script_section = self.get_script_section_and_config()['section']
        script = script_section[name]
        return self.processor.forward(script, stdin=input)

    def eval_with_input(self, name):
        def wrap(zpy_input):
            self.eval(name=name, input=zpy_input)
        return wrap

    def last_zcommand(self):
        return self.processor.last_zcommand

    """
        Modules
    """
    def get_modules(self):
        return self.get_section(section=self.MODULE)
    def remove_module(self, name):
        return self.remove_from_section(section=self.MODULE, name=name)
    def add_module(self, name, module):
        return self.add_to_section(self.MODULE, name, module)
    def get_module_dict(self):
        section = self.get_section_and_config(self.MODULE)['section']
        return section

    """
        Default imports
    """
    def get_def_imports(self):
        return self.get_section(section=self.DEFAULT_IMPORTS)
    def remove_def_imports(self, name):
        return self.remove_from_section(section=self.DEFAULT_IMPORTS, name=name)
    def add_def_imports(self, name, module):
        return self.add_to_section(self.DEFAULT_IMPORTS, name, module)
    def get_def_imports_dict(self):
        section = self.get_section_and_config(self.DEFAULT_IMPORTS)['section']
        return section
