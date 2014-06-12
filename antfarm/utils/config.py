
from antfarm.base import App

from configparser import ConfigParser

class ConfigApp(App):
    '''
    App sub-class which retrieves various config options from a ini file.
    '''
    def __init__(self, *args, **kwargs):
        config = ConfigParser()
        config.read(kwargs['config_file'])
        for section on config.sections():
            kwargs[section] = dict(config.items(section))

        super().__init__(*args, **kwargs)

