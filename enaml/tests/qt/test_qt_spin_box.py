#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from uuid import uuid4

from enaml.qt.qt.QtGui import QApplication
from enaml.qt.qt_spin_box import QtSpinBox
from enaml.qt.qt_local_pipe import QtLocalPipe

class TestQtSpinBox(object):
    """ Unit tests for the QtSpinBox

    """
    def __init__(self):
        """ Create an application instance so that widgets can be created

        """
        if not QApplication.instance():
            self.app = QApplication([])
    
    def setUp(self):
        """ Set up the widget for testing

        """
        self.spin_box = QtSpinBox(None, uuid4().hex, QtLocalPipe(),
                                  QtLocalPipe())
        self.spin_box.create()

    def test_set_maximum(self):
        """ Test the QtSpinBox's set_maximum command

        """
        maximum = 50
        self.spin_box.recv('set_maximum', {'value':maximum})
        assert self.spin_box.widget.maximum() == maximum

    def test_set_minimum(self):
        """ Test the QtSpinBox's set_minimum command

        """
        minimum = 10
        self.spin_box.recv('set_minimum', {'value':minimum})
        assert self.spin_box.widget.minimum() == minimum

    def test_set_single_step(self):
        """ Test the QtSpinBox's set_single_step command

        """
        step = 5
        self.spin_box.recv('set_single_step', {'value':step})
        assert self.spin_box.widget.singleStep() == step

    def test_set_tracking(self):
        """ Test the QtSpinBox's set_tracking command

        """
        tracking = False
        self.spin_box.recv('set_tracking', {'value':tracking})
        assert self.spin_box.widget.keyboardTracking() == tracking

    def test_set_validator(self):
        """ Test the QtSpinBox's set_validator command

        """
        # XXX
        #validator = ???
        #self.spin_box.recv('set_validator', {'value':validator})
        #assert self.spin_box.widget.validator() == validator
        pass

    def test_set_value(self):
        """ Test the QtSpinBox's set_value command

        """
        value = 20
        self.spin_box.recv('set_value', {'value':value})
        assert self.spin_box.widget.value() == value

    def test_set_wrap(self):
        """ Test the QtSpinBox's set_wrap command

        """
        wrap = True
        self.spin_box.recv('set_wrap', {'value':wrap})
        assert self.spin_box.widget.wrapping() == wrap
