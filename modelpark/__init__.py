import os
from .modelpark import ModelPark

here = os.path.abspath(os.path.dirname(__file__))
print (here)
print (os.path.join(here, "VERSION"))
def get_version():
    version_path = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, "VERSION"), "r") as fh:
        app_version = fh.read().strip()
        return app_version

__version__ = get_version()

def version():
    return get_version()
