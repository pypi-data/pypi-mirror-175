import setuptools.build_meta

class WrongPackageIndexError(Exception):
    pass

def get_requires_for_build_sdist(config_settings=None):
    return setuptools.build_meta.get_requires_for_build_sdist(config_settings)

def build_sdist(sdist_directory, config_settings=None):
    return setuptools.build_meta.build_sdist(sdist_directory, config_settings)

def get_requires_for_build_wheel(config_settings=None):
    raise WrongPackageIndexError("Please install this package from the Neuron package index @ pip.repos.neuron.amazonaws.com")
   
