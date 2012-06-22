#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from .qt.QtGui import QLineEdit
from .qt.QtCore import Signal
from .qt_control import QtControl
from .qt_enaml_validator import QtEnamlValidator

PASSWORD_MODE = {
    'normal': QLineEdit.Normal,
    'password' : QLineEdit.Password,
    'silent' : QLineEdit.NoEcho
}

class QtEnamlLineEdit(QLineEdit):
    """ A QLineEdit subclass which converts a lost focus event into 
    a lost focus signal.

    """
    lostFocus = Signal()

    def focusOutEvent(self, event):
        self.lostFocus.emit()
        return super(QtEnamlLineEdit, self).focusOutEvent(event)

class QtField(QtControl):
    """ A Qt implementation of a field (called QLineEdit in Qt)

    """
    def create(self, parent):
        """ Create underlying widget

        """
        self.widget = QtEnamlLineEdit(parent)
        self.widget.show()

    def initialize(self, init_attrs):
        """ Initialize the attributes of the widget

        """
        self.set_max_length(init_attrs.get('max_length'))
        self.set_password_mode(init_attrs.get('password_mode'))
        self.set_placeholder_text(init_attrs.get('placeholder_text'))
        self.set_read_only(init_attrs.get('read_only'))
        self.set_submit_mode(init_attrs.get('submit_mode'))
        self.set_text(init_attrs.get('text'))
        self.set_validator(init_attrs.get('validator'))

    def bind(self):
        """ Connect the widget's signals to slots

        """
        self.widget.lostFocus.connect(self.on_lost_focus)
        self.widget.returnPressed.connect(self.on_return_pressed)
        self.widget.textEdited.connect(self.on_text_edited)

    #--------------------------------------------------------------------------
    # Event Handlers
    #--------------------------------------------------------------------------
    def on_lost_focus(self):
        """ Event handler for lost_focus

        """
        self.send('lost_focus', {})

    def on_return_pressed(self):
        """ Event handler for return_pressed

        """
        self.send('return_pressed', {})

    def on_text_edited(self):
        """ Event handler for text_edited

        """
        self.send('text_edited', {})

    #--------------------------------------------------------------------------
    # Message Handlers
    #--------------------------------------------------------------------------
    def receive_set_max_length(self, ctxt):
        """ Message handler for set_max_length

        """
        length = ctxt.get('value')
        if length is not None:
            self.set_max_length(length)

    def receive_set_password_mode(self, ctxt):
        """ Message handler for set_password_mode

        """
        mode = ctxt.get('value')
        if mode is not None:
            self.set_password_mode(mode)

    def receive_set_placeholder_text(self, ctxt):
        """ Message handler for set_placeholder_text

        """
        text = ctxt.get('value')
        if text is not None:
            self.set_placeholder_text(text)

    def receive_set_read_only(self, ctxt):
        """ Message handler for set_read_only

        """
        read_only = ctxt.get('value')
        if read_only is not None:
            self.set_read_only(read_only)

    def receive_set_submit_mode(self, ctxt):
        """ Message handler for set_submit_mode

        """
        mode = ctxt.get('value')
        if mode is not None:
            self.set_submit_mode(mode)

    def receive_set_text(self, ctxt):
        """ Message handler for set_text

        """
        text = ctxt.get('value')
        if text is not None:
            self.set_text(text)

    def receive_set_validator(self, ctxt):
        """ Message handler for set_validator

        """
        val = ctxt.get('value')
        if val is not None:
            self.set_validator(val)

    #--------------------------------------------------------------------------
    # Widget Update Methods
    #--------------------------------------------------------------------------
    def set_max_length(self, length):
        """ Set the maximum length of the field

        """
        if length <= 0 or length > 32767:
            length = 32767

        self.widget.setMaxLength(length)

    def set_password_mode(self, mode):
        """ Set the password mode of the field

        """
        self.widget.setEchoMode(PASSWORD_MODE[mode])

    def set_placeholder_text(self, text):
        """ Set the placeholder text of the field

        """
        self.widget.setPlaceholderText(text)

    def set_read_only(self, read_only):
        """ Set whether or not the field is read only

        """
        self.widget.setReadOnly(read_only)

    def set_submit_mode(self, mode):
        """ Set the submit mode of the field

        """
        # XXX Qt implementation?
        pass

    def set_text(self, text):
        """ Set the text of the field

        """
        self.widget.setText(text)

    def set_validator(self, val):
        """ Set the field's validator

        """
        validator = QtEnamlValidator(val)
        self.widget.setValidator(validator)