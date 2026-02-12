from .modelpark import ModelPark
from .modelpark import APIManager


def get_version():
    app_version = '0.2.0'
    cli_version = 'github-releases'
    version = {
        'app_version': app_version,
        'cli_version': cli_version,
    }
    return version


__version__ = get_version()


def version():
    return get_version()
