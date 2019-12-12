# -*- coding: utf-8 -*-

"""
Comboboxes
==========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtWidgets as QW

# GuiPy imports
from guipy.layouts import QW_QHBoxLayout
from guipy.widgets import (
    BaseBox, QW_QComboBox, QW_QLabel, get_box_value, get_modified_box_signal,
    set_box_value)

# All declaration
__all__ = ['DualComboBox', 'EditableComboBox']


# %% CLASS DEFINITIONS
# Make class with two comboboxes
class DualComboBox(BaseBox):
    """
    Defines the :class:`~DualComboBox` class.

    """

    # Signals
    modified = QC.Signal([], [int, int], [int, str], [str, int],
                         [str, str])

    # Initialize the DualComboBox class
    def __init__(self, editable=(False, False), sep=None, parent=None, *args,
                 **kwargs):
        """
        Initialize an instance of the :class:`~DualComboBox` class.

        Optional
        --------
        editable : tuple of bool. Default: (False, False)
            A tuple containing editability of each combobox.
        sep : str or None. Default: None
            The string that must be used as a separator between the two
            comboboxes. If *None*, no separator is used.
        parent : :obj:`~PyQt5.QtWidgets.QWidget` object or None. Default: None
            The parent widget to use for this dual combobox or *None* for no
            parent.

        """

        # Call super constructor
        super().__init__(parent)

        # Create the dual combobox
        self.init(editable, sep, *args, **kwargs)

    # Override __getitem__ to return the left and/or right combobox
    def __getitem__(self, key):
        # If key is a slice object, return everything that is requested
        if isinstance(key, slice):
            return(tuple([self[i] for i in range(*key.indices(2))]))

        # If key is an integer, return the corresponding combobox
        elif isinstance(key, int):
            # If key is zero, return left_box
            if(key == 0):
                return(self.left_box)
            # Else, if key is one, return right_box
            elif(key == 1):
                return(self.right_box)
            # Else, raise IndexError
            else:
                raise IndexError("Index out of range")

        # Else, raise TypeError
        else:
            raise TypeError("Index must be of type 'int' or 'slice', not type "
                            "%r" % (type(key).__name__))

    # This function sets up the dual combobox
    def init(self, editable, sep):
        """
        Sets up the dual combobox after it has been initialized.

        """

        # Create the box_layout
        box_layout = QW_QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create two comboboxes with the provided editability
        # LEFT
        left_box = EditableComboBox() if editable[0] else QW_QComboBox()
        get_modified_box_signal(left_box).connect(self.emit_modified_signal)
        box_layout.addWidget(left_box)
        self.left_box = left_box

        # RIGHT
        right_box = EditableComboBox() if editable[1] else QW_QComboBox()
        get_modified_box_signal(right_box).connect(self.emit_modified_signal)
        box_layout.addWidget(right_box)
        self.right_box = right_box

        # If sep is not None, create label and add it
        if sep is not None:
            sep_label = QW_QLabel(sep)
            sep_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
            box_layout.insertWidget(1, sep_label)

    # This function emits an extra modified signal
    @QC.Slot()
    def emit_modified_signal(self):
        # Emit modified signal with proper types
        for types in [(int, int), (int, str), (str, int), (str, str)]:
            self.modified[types[0], types[1]].emit(
                get_box_value(self.left_box, types[0]),
                get_box_value(self.right_box, types[1]))

    # This function retrieves a value of this special box
    def get_box_value(self, *args):
        """
        Returns the current values of this dual combobox as a tuple.

        Returns
        -------
        value : tuple
            A tuple containing the values of the comboboxes, formatted as
            `(left, right)`.

        """

        return(get_box_value(self.left_box, *args),
               get_box_value(self.right_box, *args))

    # This function sets the value of this special box
    def set_box_value(self, value):
        """
        Sets the current value of the dual combobox to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the comboboxes, formatted as
            `(left, right)`.

        """

        set_box_value(self.left_box, value[0])
        set_box_value(self.right_box, value[1])


# Create custom QComboBox class that is editable
class EditableComboBox(QW_QComboBox):
    """
    Defines the :class:`~QW_QEditableComboBox` class.

    This class makes the :class:`~guipy.widgets.QW_QComboBox` class editable.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        self.completer().setCompletionMode(QW.QCompleter.PopupCompletion)
        self.completer().setFilterMode(QC.Qt.MatchContains)
