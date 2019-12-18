# -*- coding utf-8 -*-

"""
Plot Types
==========

"""


# %% IMPORTS
# Import core modules
from . import base, core
from .base import *
from .core import *

# Import base modules

# Import subpackages
from . import plot_props

# All declaration
__all__ = ['base', 'core', 'plot_props']
__all__.extend(base.__all__)
__all__.extend(core.__all__)

# Author declaration
__author__ = "Ellert van der Velden (@1313e)"