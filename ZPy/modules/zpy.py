import configparser

class zpy():
    #Constants
    SCRIPTS = "SCRIPTS"
    MODULE = "MODULE"
    DEFAULT_IMPORTS = "DEFAULT_IMPORTS"
    def __init__(self, processor):
        self.config_file = "zpy.conf"
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str
        self.processor = processor

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
        print(script[236:240])
        return self.add_to_section(self.SCRIPTS, name, value=script)



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


    """
        Common methods
    """

    def read_config(self):
       self.config.read(self.config_file)

    def get_config(self):
        self.read_config()
        return self.config

    def save_config(self, config):
        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

    def get_script_section_and_config(self):
        return self.get_section_and_config(self.SCRIPTS)
    def get_module_section_and_config(self):
        return self.get_section_and_config(self.MODULE)
    def get_section_and_config(self, section):
        config = self.get_config()
        sections = config.sections()
        if section not in sections:
            config.add_section(section)
        return {
            'section': config[section],
            'config': config
        }

    def add_to_section(self, section, name, value):
        #script_section_and_config = self.get_script_section_and_config()
        section_and_config = self.get_section_and_config(section)
        section_and_config['section'][name] = value
        self.save_config(section_and_config['config'])
        return ""

    def get_section(self, section):
        section = self.get_section_and_config(section)['section']
        res = []
        for name, item in section.items():
            res.append("%s => %s" % (name, item))
        return "\n".join(res)

    def remove_from_section(self,section,name):
        section_and_config = self.get_section_and_config(section)
        section_and_config['config'].remove_option(section, name)
        self.save_config(section_and_config['config'])
        return ""