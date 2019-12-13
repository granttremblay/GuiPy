# -*- coding: utf-8 -*-

"""
Widgets Core
============
Provides a collection of utility functions and the :class:`~BaseBox` class
definition, which are core to the functioning of all widgets.

"""


# %% IMPORTS
# Package imports
import numpy as np
from qtpy import QtCore as QC, QtGui as QG, QtWidgets as QW

# GuiPy imports
from guipy.widgets.base import QW_QLabel, QW_QWidget

# All declaration
__all__ = ['BaseBox', 'get_box_value', 'get_modified_box_signal',
           'set_box_value']


# %% CLASS DEFINITIONS
# Make base class for custom boxes
# As QW.QWidget is a strict class (in C++), this cannot be an ABC
class BaseBox(QW_QWidget):
    """
    Defines the :class:`~BaseBox` base class.

    This class is used by many custom :class:`~PyQt5.QtWidgets.QWidget` classes
    as their base. It defines the :attr:`~modified` signal, which is
    automatically connected to any widget that changes its state.

    """

    # Define modified signal
    modified = QC.Signal()

    # Initialize the BaseBox class
    def __init__(self, *args, **kwargs):
        # Call super constructor
        super().__init__(*args, **kwargs)

        # If the 'modified_signal_slot' slot is available, connect it
        if hasattr(self, 'modified_signal_slot'):
            self.modified.connect(self.modified_signal_slot)

    # Override childEvent to connect signals if child has a modified signal
    def childEvent(self, event):
        """
        Special :meth:`~PyQt5.QtCore.QObject.childEvent` event that
        automatically connects the default modified signal of any widget that
        becomes a child of this widget.

        """

        # If this event involved a child being added, check child object
        if(event.type() == QC.QEvent.ChildAdded):
            # Obtain child object
            child = event.child()

            # Try to obtain the modified signal of this child
            try:
                signal = get_modified_box_signal(child)
            # If this fails, it does not have one
            except NotImplementedError:
                pass
            # If this succeeds, connect it to the 'modified' signal
            else:
                signal.connect(self.modified)

        # Call and return super method
        return(super().childEvent(event))

    # This function connects a given box to the modified signal
    def connect_box(self, box):
        """
        Connect the default modified signal of the provided `box` to this
        widget's :attr:`~modified` signal.

        """

        # Check if the given box is a child of this box and skip if so
        if box in self.children():
            return

        # Obtain the modified signal of the given box
        signal = get_modified_box_signal(box)

        # Connect the signals
        signal.connect(self.modified)

    # Define get_box_value method
    def get_box_value(self, value_sig=None):
        """
        Obtain the value of this widget and return it.

        """

        raise NotImplementedError(self.__class__)

    # Define set_box_value method
    def set_box_value(self, value):
        """
        Set the value of this widget to `value`.

        """

        raise NotImplementedError(self.__class__)


# %% FUNCTION DEFINITIONS
# This function gets the value of a provided box
def get_box_value(box, *value_sig):
    """
    Retrieves the value of the provided widget `box` and returns it.

    Parameters
    ----------
    box : :obj:`~PyQt5.QtWidgets.QWidget` object
        The widget whose value must be returned.
    value_sig : positional arguments of type
        The signature of the value of `box` that must be returned.
        If empty or invalid, the default value is returned.
        If `box` is an instance of :class:`~BaseBox`, this argument is passed
        to :meth:`~BaseBox.get_box_value`.

    Returns
    -------
    box_value : obj
        The value of the requested `box`.

    """

    # Values (QAbstractSpinBox)
    if isinstance(box, QW.QAbstractSpinBox):
        return(box.value())

    # Bools/Buttons (QAbstractButton)
    elif isinstance(box, QW.QAbstractButton):
        if box.isCheckable() and str not in value_sig:
            return(box.isChecked())
        else:
            return(box.text())

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        return(box.currentIndex() if int in value_sig else box.currentText())

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        return(box.text())

    # Labels (QLabel)
    elif isinstance(box, QW.QLabel):
        for attr in ['movie', 'picture', 'pixmap']:
            if getattr(box, attr)() is not None:
                return(getattr(box, attr)())
        else:
            return(box.text())

    # Custom boxes (BaseBox)
    elif isinstance(box, BaseBox):
        return(box.get_box_value(*value_sig))

    # If none applies, raise error
    else:
        raise NotImplementedError("Custom boxes must be a subclass of BaseBox")


# This function gets the emitted signal when a provided box is modified
def get_modified_box_signal(box, *signal_sig):
    """
    Retrieves a signal of the provided widget `box` that indicates that `box`
    has been modified and returns it.

    Parameters
    ----------
    box : :obj:`~PyQt5.QtWidgets.QWidget` object
        The widget whose modified signal must be retrieved.
    signal_sig : positional arguments of type
        The signature of the modified signal that is requested.
        If empty or invalid, the default modified signal is returned.
        If `box` is an instance of :class:`~BaseBox`, this argument has no
        effect.

    Returns
    -------
    modified_signal : :obj:`~PyQt5.QtCore.pyqtBoundSignal` object
        The requested modified signal of `box`.
        If `box` is an instance of :class:`~BaseBox`, this is always
        :attr:`~BaseBox.modified`.

    """

    # Values (QAbstractSpinBox)
    if isinstance(box, QW.QAbstractSpinBox):
        return(box.valueChanged)

    # Bools/Buttons (QAbstractButton)
    elif isinstance(box, QW.QAbstractButton):
        return(box.toggled if box.isCheckable() else box.clicked)

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        return(box.currentIndexChanged if int in signal_sig else
               box.currentTextChanged)

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        return(box.textChanged)

    # Labels (QLabel)
    elif isinstance(box, QW_QLabel):
        return(box.contentsChanged)
    elif isinstance(box, QW.QLabel):
        raise NotImplementedError("Default QW.QLabel has no modified signal "
                                  "defined. Use QW_QLabel instead!")

    # Custom boxes (BaseBox)
    elif isinstance(box, BaseBox):
        return(box.modified)

    # If none applies, raise error
    else:
        raise NotImplementedError("Custom boxes must be a subclass of BaseBox")


# This function sets the value of a provided box
def set_box_value(box, value):
    """
    Sets the value of the provided widget `box` to `value`.

    Parameters
    ----------
    box : :obj:`~PyQt5.QtWidgets.QWidget` object
        The widget whose value must be set.
    value : obj
        The value that must be set in the provided `box`.
        If `box` is an instance of :class:`~BaseBox`, this argument is passed
        to :meth:`~BaseBox.set_box_value`.

    """

    # Values (QAbstractSpinBox)
    if isinstance(box, QW.QAbstractSpinBox):
        box.setValue(value)

    # Bools/Buttons (QAbstractButton)
    elif isinstance(box, QW.QAbstractButton):
        if isinstance(value, str):
            box.setText(value)
        else:
            box.setChecked(value)

    # Items (QComboBox)
    elif isinstance(box, QW.QComboBox):
        if isinstance(value, int):
            box.setCurrentIndex(value)
        else:
            index = box.findText(value)
            if(index != -1):
                box.setCurrentIndex(index)
            else:
                box.setCurrentText(value)

    # Strings (QLineEdit)
    elif isinstance(box, QW.QLineEdit):
        box.setText(value)

    # Labels (QLabel)
    elif isinstance(box, QW.QLabel):
        if isinstance(value, str):
            box.setText(value)
        elif isinstance(value, (int, float, np.integer, np.floating)):
            box.setNum(value)
        elif isinstance(value, QG.QMovie):
            box.setMovie(value)
        elif isinstance(value, QG.QPicture):
            box.setPicture(value)
        elif isinstance(value, QG.QPixmap):
            box.setPixmap(value)
        else:
            raise TypeError("QLabel does not support the given type")

    # Custom boxes (BaseBox)
    elif isinstance(box, BaseBox):
        box.set_box_value(value)

    # If none applies, raise error
    else:
        raise NotImplementedError("Custom boxes must be a subclass of BaseBox")
