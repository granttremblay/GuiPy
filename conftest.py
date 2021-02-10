# -*- coding: utf-8 -*-

# %% IMPORTS
# Package imports
import matplotlib as mpl
from py.path import local


# Set MPL backend
mpl.use('Agg')


# %% PYTEST CUSTOM CONFIGURATION PLUGINS
# This makes the pytest report header mention the tested GuiPy version
def pytest_report_header(config):
    from guipy.__version__ import __version__
    return("GuiPy: %s" % (__version__))


# %% PYTEST SETTINGS
# Set the current working directory to the temporary directory
local.get_temproot().chdir()
