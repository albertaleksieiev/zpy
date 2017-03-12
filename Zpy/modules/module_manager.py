import importlib.util

from Zpy.modules.helpful.zpy import zpy
from Zpy.modules.helpful.zjs import zjs


class ModuleManager():
    def __init__(self):
        self.modules = None
        self.last_modules_dict = None
    def is_storage_changed(self):
        ##TODO Optimize list comparing
        return self.modules == None

    def refetch(self, processor):
        if self.modules == None:
            self.modules = {
                'zpy': zpy(processor=processor),
                'zjs': zjs(processor=processor)
            }
            modules = self.modules['zpy'].get_module_dict()

            #For comparing - in is_storage_changed method
            self.last_modules_dict = modules



            for name, module in modules.items():
                spec = importlib.util.spec_from_file_location(name, module)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                self.modules[name] = mod

        return self.modules

    def get_modules(self, processor):
        if self.is_storage_changed():
            return self.refetch(processor=processor)

        return self.modules
