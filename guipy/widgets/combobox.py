# -*- coding: utf-8 -*-

"""
Comboboxes
==========

"""


# %% IMPORTS
# Built-in imports

# Package imports
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy import INT_TYPES
from guipy import layouts as GL, widgets as GW
from guipy.widgets import get_box_value, set_box_value

# All declaration
__all__ = ['ComboBoxValidator', 'DualComboBox', 'EditableComboBox']


# %% CLASS DEFINITIONS
# Define the ComboBoxValidator class
class ComboBoxValidator(QG.QRegularExpressionValidator):
    # Initialize the ListValidator class
    def __init__(self, combobox_obj, regexp=None, parent=None):
        """
        Initialize an instance of the :class:`~ComboBoxValidator` class.

        Parameters
        ----------
        combobox_obj : :obj:`~PyQt5.QtWidgets.ComboBox`
            Combobox object for which the editable line must be validated.

        Optional
        --------
        regexp : str or None. Default: None
            The regular expression pattern to use for validating an input
            string if it is not found in `combobox_obj`.
            If *None*, no regular expression is used.
        parent : :obj:`~PyQt5.QtCore.QObject` object or None. Default: None
            The parent object to use for this validator or *None* for no
            parent.

        """

        # Save the completer of the provided combobox
        self.completer = combobox_obj.completer()

        # Check provided regexp
        if regexp is None:
            # If regexp is None, set the pattern to one that rejects all
            regexp = r"$.^"

        # Call super constructor
        super().__init__(QC.QRegularExpression(regexp), parent)

    # Override validate to first check the combobox completer
    def validate(self, string, pos):
        # Check if string is already in the completions list
        index = self.completer.completionModel().index(0, 0)
        match = self.completer.completionModel().match(
            index, QC.Qt.EditRole, string, flags=QC.Qt.MatchExactly)

        # Check if there is a match
        if not match:
            # If not, set the completion prefix in the completer
            self.completer.setCompletionPrefix(string)

        # Obtain the current completion string
        completion = self.completer.currentCompletion()

        # Check the completion string against the given one and act accordingly
        if completion:
            # If the completion string is not empty, check if it matches
            if match and string:
                # If so, it is acceptable
                state = self.Acceptable
            else:
                # Else, it is intermediate
                state = self.Intermediate

            # Return the state, string and pos
            return(state, string, pos)
        else:
            # If the completion string is empty, use the regular expression
            return(super().validate(string, pos))


# Make class with two comboboxes
class DualComboBox(GW.BaseBox):
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
            A tuple containing the editability of each combobox.
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
        # If key is an integer, return the corresponding combobox
        if isinstance(key, INT_TYPES):
            # If key is 0 or -2, return left_box
            if key in (0, -2):
                return(self.left_box)
            # Else, if key is 1 or -1, return right_box
            elif key in (1, -1):
                return(self.right_box)
            # Else, raise IndexError
            else:
                raise IndexError("Index out of range")

        # If key is a slice object, return everything that is requested
        elif isinstance(key, slice):
            return(*map(self.__getitem__, range(*key.indices(2))),)

        # Else, raise TypeError
        else:
            raise TypeError("Index must be of type 'int' or 'slice', not type "
                            "%r" % (type(key).__name__))

    # This property returns the default 'modified' signal
    @property
    def default_modified_signal(self):
        return(self.modified[str, str])

    # This function sets up the dual combobox
    def init(self, editable, sep):
        """
        Sets up the dual combobox after it has been initialized.

        """

        # Create the box_layout
        box_layout = GL.QHBoxLayout(self)
        box_layout.setContentsMargins(0, 0, 0, 0)

        # Create two comboboxes with the provided editability
        # LEFT
        left_box = EditableComboBox() if editable[0] else GW.QComboBox()
        box_layout.addWidget(left_box)
        self.left_box = left_box

        # RIGHT
        right_box = EditableComboBox() if editable[1] else GW.QComboBox()
        box_layout.addWidget(right_box)
        self.right_box = right_box

        # If sep is not None, create label and add it
        if sep is not None:
            sep_label = GW.QLabel(sep)
            sep_label.setSizePolicy(QW.QSizePolicy.Fixed, QW.QSizePolicy.Fixed)
            box_layout.insertWidget(1, sep_label)

    # This function is automatically called whenever 'modified' is emitted
    @QC.Slot()
    def modified_signal_slot(self):
        # Emit modified signal with proper types
        for types in [(int, int), (int, str), (str, int), (str, str)]:
            self.modified[types[0], types[1]].emit(
                *DualComboBox.get_box_value(self, *types))

    # This function retrieves a value of this special box
    def get_box_value(self, *value_sig):
        """
        Returns the current values of this dual combobox as a tuple.

        Returns
        -------
        value : tuple
            A tuple containing the values of the comboboxes, formatted as
            `(left, right)`.

        """

        # If value_sig contains more than 1 element, use them separately
        if(len(value_sig) > 1):
            return(get_box_value(self.left_box, value_sig[0]),
                   get_box_value(self.right_box, value_sig[1]))
        else:
            return(get_box_value(self.left_box, *value_sig),
                   get_box_value(self.right_box, *value_sig))

    # This function sets the value of this special box
    def set_box_value(self, value, *args, **kwargs):
        """
        Sets the current value of the dual combobox to `value`.

        Parameters
        ----------
        value : tuple
            A tuple containing the values of the comboboxes, formatted as
            `(left, right)`.

        """

        set_box_value(self.left_box, value[0], *args, **kwargs)
        set_box_value(self.right_box, value[1], *args, **kwargs)


# Create custom QComboBox class that is editable
class EditableComboBox(GW.QComboBox):
    """
    Defines the :class:`~QEditableComboBox` class.

    This class makes the :class:`~guipy.widgets.QComboBox` class editable.

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        self.completer().setCompletionMode(QW.QCompleter.PopupCompletion)
        self.completer().setFilterMode(QC.Qt.MatchContains)
