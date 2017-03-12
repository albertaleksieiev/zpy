import configparser
class z_base:
    SCRIPTS = "SCRIPTS"
    MODULE = "MODULE"
    DEFAULT_IMPORTS = "DEFAULT_IMPORTS"
    def __init__(self, processor):
        self.config_file = "zpy.conf"
        self.config = configparser.RawConfigParser()
        self.config.optionxform = str
        self.processor = processor
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
        # script_section_and_config = self.get_script_section_and_config()
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

    def remove_from_section(self, section, name):
        section_and_config = self.get_section_and_config(section)
        section_and_config['config'].remove_option(section, name)
        self.save_config(section_and_config['config'])
        return ""

