import os
from .modelpark import ModelPark
from .modelpark import APIManager
from .modelpark import Install_ModelPark_CLI

def get_version():
    #version_path = os.path.abspath(os.path.dirname(__file__))
    #with open(os.path.join(here, "VERSION"), "r") as fh:
        app_version = '0.1.17'
        cli_version = '0.1.2'
        version = {'app_version':app_version,
                   'cli_version':cli_version,
                   }
        return version

__version__ = get_version()

def version():
    return get_version()
