# -*- coding: utf-8 -*-

"""
EntriesBoxes
============

"""


# %% IMPORTS
# Built-in imports


# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW
from sortedcontainers import SortedDict as sdict, SortedSet as sset

# GuiPy imports
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, get_modified_signal, set_box_value

# All declaration
__all__ = ['EditableEntriesBox']


# %% CLASS DEFINITIONS
# Make class for creating editable entry lists
class EditableEntriesBox(GW.BaseBox):
    """
    Defines the :class:`~EditableEntriesBox` class.

    This widget allows for a series of 'list' entries to be maintained within a
    single box, and is basically a Qt-version of a Python dict.
    Entries that must use a specific widget can be added using the
    :meth:`~addEntryTypes` method, whereas disallowed entry names can be added
    with :meth:`~addBannedNames`.

    """

    # Signals
    modified = QC.Signal([], [dict])

    # Initialize the EditableEntriesBox class
    def __init__(self, parent=None):
        """
        Initialize an instance of the :class:`~EditableEntriesBox` class.

        Optional
        --------
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this entries box or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the entries box
        self.init()

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[dict])

    # This property returns the number of entries in the box
    def entryCount(self):
        return((self.entries_grid.count()//3)-1)

    # This function creates the entries box
    def init(self):
        """
        Sets up the entries box after it has been initialized.

        """

        # Set the height of a single entry
        self.entry_height = 24

        # Create empty dict of non-generic entry types
        self.entry_types = {}

        # Create empty set of banned entry names
        self.banned_names = sset()

        # Create the box_layout
        box_layout = GL.QVBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create the entries_grid
        entries_grid = GL.QGridLayout()
        entries_grid.setColumnStretch(1, 1)
        entries_grid.setColumnStretch(2, 2)
        box_layout.addLayout(entries_grid)
        self.entries_grid = entries_grid

        # Add a header
        entries_grid.addWidget(GW.QLabel(""), 0, 0)
        entries_grid.addWidget(GW.QLabel("Entry name"), 0, 1)
        entries_grid.addWidget(GW.QLabel("Entry value"), 0, 2)

        # Add an 'Add'-button
        add_but = GW.QToolButton()
        add_but.setFixedSize(self.entry_height, self.entry_height)
        add_but.setToolTip("Add new entry")
        get_modified_signal(add_but).connect(self.add_entry)
        box_layout.addWidget(add_but)

        # If this theme has an 'add' icon, use it
        if QG.QIcon.hasThemeIcon('add'):
            add_but.setIcon(QG.QIcon.fromTheme('add'))
        # Else, use a simple plus
        else:
            add_but.setText('+')

        # Add a stretch
        box_layout.addStretch()

        # Set a minimum width for the first column
        self.entries_grid.setColumnMinimumWidth(0, self.entry_height)

    # This function is called whenever a new entry is added
    @QC.Slot()
    def add_entry(self):
        """
        Adds a new entry to the entries box.

        """

        # Create a combobox with the name of the entry
        name_box = GW.EditableComboBox()
        name_box.addItems(self.entry_types.keys())
        set_box_value(name_box, -1)
        get_modified_signal(name_box).connect(
            lambda: self.create_value_box(name_box))

        # Create a 'Delete'-button
        del_but = GW.QToolButton()
        del_but.setFixedSize(self.entry_height, self.entry_height)
        del_but.setToolTip("Delete this entry")
        get_modified_signal(del_but).connect(
            lambda: self.remove_entry(name_box))

        # If this theme has a 'remove' icon, use it
        if QG.QIcon.hasThemeIcon('remove'):
            del_but.setIcon(QG.QIcon.fromTheme('remove'))
        # Else, use a standard icon
        else:
            del_but.setIcon(del_but.style().standardIcon(
                QW.QStyle.SP_DialogCloseButton))

        # Add a new row to the grid layout
        next_row = self.entries_grid.getItemPosition(
            self.entries_grid.count()-1)[0]+1
        self.entries_grid.addWidget(del_but, next_row, 0)
        self.entries_grid.addWidget(name_box, next_row, 1)
        self.entries_grid.addWidget(GW.QWidget(), next_row, 2)

    # This function is called whenever an entry must be removed
    @QC.Slot(GW.QComboBox)
    def remove_entry(self, name_box):
        """
        Removes the entry associated with the provided `name_box` from the
        entries box.

        """

        # Determine at what index the provided name_box currently is in grid
        index = self.entries_grid.indexOf(name_box)

        # As every entry contains 3 items, remove item 3 times at index-1
        for _ in range(3):
            # Remove the current item at index-1
            item = self.entries_grid.takeAt(index-1)

            # Close the widget in this item and delete it
            item.widget().close()
            del item

    # This function is called whenever a new entry field box is requested
    @QC.Slot(GW.QComboBox)
    def create_value_box(self, name_box):
        """
        Creates a value box for the provided `name_box` and its corresponding
        current value, and replaces the current value box with it.

        """

        # Determine the current value of the name_box
        entry_name = get_box_value(name_box)

        # Determine at what index the provided name_box currently is in grid
        index = self.entries_grid.indexOf(name_box)

        # Retrieve which value_box is currently there
        cur_box = self.entries_grid.itemAt(index+1).widget()

        # Obtain the widget class associated with this entry_name
        if entry_name:
            # If the entry name is given, obtain it from dict or use default
            new_box_class = self.entry_types.get(entry_name, GW.GenericBox)
        else:
            # If the entry name is not given, use an empty widget
            new_box_class = GW.QWidget

        # If the current value box is not this box type already, replace it
        if type(cur_box) is not new_box_class:
            # If not, create new value box
            new_box = new_box_class()

            # Replace cur_box with new_box
            item = self.entries_grid.replaceWidget(cur_box, new_box)

            # Close the widget in this item and delete it
            item.widget().close()
            del item

    # This function adds a list of names to the banned names set
    def addBannedNames(self, banned_names):
        """
        Adds the given `banned_names` list to the set of names that are banned
        from being used as entry names.

        Parameters
        ----------
        banned_names : list of str
            List containing entry names that are not allowed.

        """

        # Convert banned_names to a set
        banned_names = sset(banned_names)

        # Make sure that '' is not in banned_names
        banned_names.discard('')

        # Update the current set of banned names
        self.banned_names.update(banned_names)

        # Determine if there are any types in entry_types that are now banned
        banned_types = banned_names.intersection(self.entry_types.keys())

        # Remove all new banned types from entry_types
        for banned_type in banned_types:
            self.entry_types.pop(banned_type)

    # This function updates the entry types dict with a given dict
    def addEntryTypes(self, entry_types):
        """
        Adds the given `entry_types` dict to the dict of entry names that use a
        specific callable when entered.

        Parameters
        ----------
        entry_types : dict
            Dict with the entry names that use a specific callable for
            obtaining the :obj:`~PyQt5.QtWidgets.QWidget` object to be used in
            the entries box.
            This dict is formatted as `{'<entry_name>': <callable>}`.

        """

        # Make sure that '' is not in entry_types
        entry_types.pop('', None)

        # Obtain the set of types in entry_types that are currently banned
        banned_types = self.banned_names.intersection(entry_types.keys())

        # Remove these banned entries from entry_types
        for banned_type in banned_types:
            entry_types.pop(banned_type)

        # Update the current dict of entry types
        self.entry_types.update(entry_types)

    # This function retrieves the values of the entries in this entries box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this entries box as a dict.

        Returns
        -------
        entries_dict : dict
            A dict with the entries currently in this entries box, formatted as
            `{'<entry_name>': <entry_value>}`.

        """

        # Create an empty dict to hold the entry values in
        entries_dict = sdict()

        # Loop over all entries in the entries grid and save them to the dict
        for i in range(3, 3*(self.entryCount()+1), 3):
            # Obtain the name of this entry
            name_box = self.entries_grid.itemAt(i+1).widget()
            entry_name = get_box_value(name_box)

            # If the entry_name is empty, skip this entry
            if not entry_name:
                continue

            # Obtain the value of this entry
            value_box = self.entries_grid.itemAt(i+2).widget()
            entry_value = get_box_value(value_box)

            # Add this entry to the dict
            entries_dict[entry_name] = entry_value

        # Return entries_dict
        return(entries_dict)

    # This function sets the values of the entries in this entries box
    def set_box_value(self, entries_dict, *value_sig):
        """
        Sets the values of the entries in this entries box to the provided
        `entries_dict`.

        Parameters
        ----------
        entries_dict : dict
            A dict containing all entries that must be set in this entries box,
            formatted as `{<entry_name>: <entry_value>}`.

        """

        # Create empty dict for all current entries
        cur_entries_dict = {}

        # Remove all entries from the entries box
        for _ in range(self.entryCount()):
            # Obtain the name of the next entry
            name_box = self.entries_grid.itemAt(4).widget()
            entry_name = get_box_value(name_box)

            # Delete this entry if it is not in entries_dict or if it is banned
            if(entry_name not in entries_dict or not entry_name or
               entry_name in self.banned_names):
                self.remove_entry(name_box)
                continue

            # Add this entry to cur_entries_dict
            cur_entries_dict[entry_name] =\
                [self.entries_grid.takeAt(3) for _ in range(3)]

        # Add all entries in entries_dict
        for row, (entry_name, entry_value) in enumerate(entries_dict.items(),
                                                        1):
            # Check if this entry_name is in cur_entries_dict
            if entry_name in cur_entries_dict:
                # If so, put it back into the entries box
                for col, item in enumerate(cur_entries_dict.pop(entry_name)):
                    self.entries_grid.addItem(item, row, col)
            else:
                # If not, add a new empty entry to the entries box
                self.add_entry()

                # Set the name of this entry
                name_box = self.entries_grid.itemAtPosition(row, 1).widget()
                set_box_value(name_box, entry_name)

            # Set the value of this entry
            value_box = self.entries_grid.itemAtPosition(row, 2).widget()
            set_box_value(value_box, entry_value)
