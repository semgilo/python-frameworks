import configparser

class MyConfigParser(configparser.ConfigParser):
    def __init__(self, defaults=None, allow_no_value=True):
        configparser.ConfigParser.__init__(self, defaults=defaults,
                                           allow_no_value=allow_no_value)

    def optionxform(self, optionstr):
        return optionstr


class ConfigHelper:
    """docstring for ConfigHelper"""
    def __init__(self):
        super(ConfigHelper, self).__init__()
        self._cps = []

    def add_cp(self, cp):
        self._cps.append(cp)

    def add_cp_by_path(self, path):
        cp = MyConfigParser()
        cp.read(path)
        self.add_cp(cp)

    def get(self, section, option):
        for cp in self._cps:
            if cp.has_section(section) and cp.has_option(section, option):
                return cp.get(section, option)
        return None

    def options(self, section):
        for cp in self._cps:
            if cp.has_section(section):
                return cp.options(section)
        return None
