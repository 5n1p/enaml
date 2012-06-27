#------------------------------------------------------------------------------
#  Copyright (c) 2012, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import os
from uuid import uuid4

from enaml.qt.qt.QtGui import QApplication
from enaml.qt.qt_directory_dialog import QtDirectoryDialog
from enaml.qt.qt_local_pipe import QtLocalPipe

class TestQtDirectoryDialog(object):
    """ Unit tests for the QtDirectoryDialog
    
    """
    def __init__(self):
        """ Create an application instance so that widgets can be created

        """
        if not QApplication.instance():
            self.app = QApplication([])
            
    def setUp(self):
        """ Set up the widget for testing

        """
        self.dir_dialog = QtDirectoryDialog(None, uuid4().hex, QtLocalPipe(),
                                            QtLocalPipe())
        self.dir_dialog.create()

    def test_set_directory(self):
        """ Test the QtDirectoryDialog's set_directory command

        """
        # The test will fail if this directory does not exist, so we use
        # the current directory to ensure that it exists
        dir_path = os.path.abspath(os.path.curdir)
        self.dir_dialog.recv('set_directory', {'value':dir_path})
        widget_path = self.dir_dialog.widget.directory().absolutePath()
        assert widget_path == dir_path
