import os
from .modelpark import ModelPark
from .modelpark import APIManager

def get_version():
    #version_path = os.path.abspath(os.path.dirname(__file__))
    #with open(os.path.join(here, "VERSION"), "r") as fh:
        app_version = '0.1.6'
        return app_version

__version__ = get_version()

def version():
    return get_version()
