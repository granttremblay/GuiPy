# -*- coding: utf-8 -*-

"""
Base Plugins
============
Provides a collection of custom :class:`~PyQt5.QtWidgets.QWidget` base classes
that allow for certain plugins to be standardized.

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.config import tr
from guipy.widgets.core import BaseBox

# All declaration
__all__ = ['BasePlugin', 'BasePluginWidget']


# %% CLASS DEFINITIONS
# Define base class for making plugins
class BasePlugin(object):
    # Property for title of this plugin
    @property
    def title(self):
        # Return title if it is defined, or raise error if not
        if hasattr(self, 'TITLE'):
            return(tr(self.TITLE))
        else:
            raise NotImplementedError


# Define base class for making plugin widgets
class BasePluginWidget(BaseBox, BasePlugin):
    # Property for location of this plugin widget
    @property
    def location(self):
        # Return location if it is defined, or return default if not
        return(getattr(self, 'LOCATION', QC.Qt.LeftDockWidgetArea))

    # Property for top-level menu actions of this plugin widget
    @property
    def menu_actions(self):
        # Return top-level menu actions if it is defined, or return empty dict
        return(getattr(self, 'MENU_ACTIONS', {}))

    # Property for toolbar actions of this plugin widget
    @property
    def toolbar_actions(self):
        # Return toolbar actions if it is defined, or return empty dict
        return(getattr(self, 'TOOLBAR_ACTIONS', {}))
