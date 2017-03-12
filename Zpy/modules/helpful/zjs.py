from Zpy.modules.helpful.z import z_base

class zjs(z_base):
    #Constants
    SCRIPTS = "SCRIPTS_JS"
    MODULE = "MODULE_JS"
    DEFAULT_IMPORTS = "DEFAULT_IMPORTS_JS"
    def __init__(self, processor):
        super().__init__(processor)

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


