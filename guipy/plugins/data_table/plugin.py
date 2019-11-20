# -*- coding: utf-8 -*-

"""
Data Table Plugin
=================

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.plugins.base import BasePluginWidget
from guipy.plugins.data_table.widgets import DataTableWidget
from guipy.widgets import QW_QAction, QW_QMenu

# All declaration
__all__ = ['DataTable']


# %% CLASS DEFINITIONS
# Define class for the DataTable plugin
class DataTable(BasePluginWidget):
    # Properties
    TITLE = "Data table"
    MENU_ACTIONS = {
        'File': []}
    TOOLBAR_ACTIONS = {
        'File': []}

    # Initialize DataTable plugin
    def __init__(self, parent=None, *args, **kwargs):
        # Call super constructor
        super().__init__(parent)

        # Set up the data table plugin
        self.init(*args, **kwargs)

    # This function sets up the data table plugin
    def init(self):
        # Create a layout
        layout = QW.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # Create a tab widget
        tab_widget = QW.QTabWidget()
        tab_widget.setElideMode(QC.Qt.ElideNone)
        tab_widget.setMovable(True)
        tab_widget.setTabsClosable(True)
        tab_widget.tabCloseRequested.connect(self.close_tab)

        # Add tab widget to layout
        self.tab_widget = tab_widget
        layout.addWidget(self.tab_widget)

        # Add all actions to the proper menus and toolbars
        self.add_actions()

        # Add a tab to the plugin
        self.add_tab()

    # Override closeEvent to do automatic clean-up
    def closeEvent(self, *args, **kwargs):
        # Close all tabs
        for index in reversed(range(self.tab_widget.count())):
            self.close_tab(index)

        # Call super event
        super().closeEvent(*args, **kwargs)

    # This function adds all associated actions to the menus and toolbars
    def add_actions(self):
        """


        """

        # Add new tab action to file menu/toolbar
        new_tab_act = QW_QAction(
            self, '&New...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_N,
            tooltip="New data table",
            triggered=self.add_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(new_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(new_tab_act)

        # Add separator to file menu
        self.MENU_ACTIONS['File'].append(None)

        # Add open tab action to file menu/toolbar
        open_tab_act = QW_QAction(
            self, '&Open...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_O,
            tooltip="Open data table",
            triggered=self.open_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(open_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(open_tab_act)

        # Add import tab action to file menu
        import_tab_act = QW_QAction(
            self, '&Import...',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_I,
            tooltip="Import data table",
            triggered=self.import_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(import_tab_act)

        # Add separator to file menu
        self.MENU_ACTIONS['File'].append(None)

        # Add save tab action to file menu/toolbar
        save_tab_act = QW_QAction(
            self, '&Save',
            shortcut=QC.Qt.CTRL + QC.Qt.Key_S,
            tooltip="Save data table",
            triggered=self.save_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(save_tab_act)
        self.TOOLBAR_ACTIONS['File'].append(save_tab_act)

        # Add save_as tab action to file menu
        save_as_tab_act = QW_QAction(
            self, 'Save &as...',
            shortcut=QC.Qt.CTRL + QC.Qt.SHIFT + QC.Qt.Key_S,
            tooltip="Save data table as...",
            triggered=self.save_as_tab,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(save_as_tab_act)

        # Add save_all tab action to file menu/toolbar
        save_all_tabs_act = QW_QAction(
            self, 'Sav&e all',
            shortcut=QC.Qt.CTRL + QC.Qt.ALT + QC.Qt.Key_S,
            tooltip="Save all data tables",
            triggered=self.save_all_tabs,
            role=QW_QAction.ApplicationSpecificRole)
        self.MENU_ACTIONS['File'].append(save_all_tabs_act)
        self.TOOLBAR_ACTIONS['File'].append(save_all_tabs_act)

        # Add export tab menu to file menu
        export_tab_menu = self.create_export_tab_menu()
        self.MENU_ACTIONS['File'].append(export_tab_menu)

    # This function creates the export_tab menu
    def create_export_tab_menu(self):
        # Create the menu
        export_tab_menu = QW_QMenu('Export', '&Export as...')

        # Define list with all export-formats
        formats = [('*.hdf5', 'HDF5'),
                   ('*.py', 'Python'),
                   ('*.txt', 'text')]

        # For every format, add an action to the export menu
        for ext, name in formats:
            # Create an action for this format
            act = QW_QAction(
                self, "%s (%s)" % (ext, name),
                tooltip="Export data table as %s file" % (name),
                triggered=getattr(self, 'export_as_%s' % (ext[2:])),
                role=QW_QAction.ApplicationSpecificRole)

            # Add it to the menu
            export_tab_menu.addAction(act)

        # Return the menu
        return(export_tab_menu)

    # This function adds a new data table widget
    @QC.Slot()
    def add_tab(self):
        # Create a DataTableWidget
        widget = DataTableWidget()

        # Add widget to the tab widget
        self.tab_widget.addTab(widget, "Table %i" % (self.tab_widget.count()))

        # Switch focus to the new tab
        self.tab_widget.setCurrentIndex(self.tab_widget.count()-1)

    # This function closes a data table widget
    @QC.Slot(int)
    def close_tab(self, index):
        # Obtain the DataTableWidget object associated with this widget
        widget = self.tab_widget.widget(index)

        # Close this widget
        widget.close()

        # Remove this widget from the tab widget
        self.tab_widget.removeTab(index)

    # This function opens a data table widget
    @QC.Slot()
    def open_tab(self):
        pass

    # This function imports a data table widget
    @QC.Slot()
    def import_tab(self):
        pass

    # This function saves a data table widget
    @QC.Slot()
    def save_tab(self):
        pass

    # This function saves a data table widget with chosen name
    @QC.Slot()
    def save_as_tab(self):
        pass

    # This function saves all data table widgets
    @QC.Slot()
    def save_all_tabs(self):
        pass

    # This function exports a data table as an HDF5 file
    @QC.Slot()
    def export_as_hdf5(self):
        pass

    # This function exports a data table as a Python file
    @QC.Slot()
    def export_as_py(self):
        pass

    # This function exports a data table as a text file
    @QC.Slot()
    def export_as_txt(self):
        pass

    # This function returns the data table belonging to a specified int
    @QC.Slot(int)
    def dataTable(self, index):
        """
        Returns the :obj:`~DataTableModel` object that belongs to the table
        with the provided tab `index`.

        Parameters
        ----------
        index : int
            If int, the index of the tab whose table is requested.

        Returns
        -------
        data_table : :obj:`~DataTableModel`
            The data table that belongs to the tab specified by the
            provided `index`.

        """

        # Return the data table model with the provided index
        return(self.tab_widget.widget(index).data_table.model())
