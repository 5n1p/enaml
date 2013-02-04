#------------------------------------------------------------------------------
# Copyright (c) 2013, Enthought, Inc.
# All rights reserved.
#------------------------------------------------------------------------------
from abc import ABCMeta, abstractmethod

from enaml.signaling import Signal

from .enums import AlignmentFlag, ItemFlag


class AbstractItemModel(object):
    """ An abstract base class for creating item based models.

    """
    __metaclass__ = ABCMeta

    #: A signal which should be emitted when an item changes. The
    #: payload is the row and column index of the item that changed.
    data_changed = Signal()

    #: A signal which should be emitted when the entire model changes
    #: structure. Sometimes, this can be simpler and more efficient
    #: than the other notification signals. This signal has no payload.
    model_changed = Signal()

    #: A signal which should be emitted when rows are inserted. The
    #: payload should be the index of the insert and the number of
    #: rows inserted.
    rows_inserted = Signal()

    #: A signal which should be emitted when rows are removed. The
    #: payload should be the index of the removal and the number of
    #: rows removed.
    rows_removed = Signal()

    #: A signal which should be emitted when columns are inserted. The
    #: payload should be the index of the insert and the number of
    #: columns inserted.
    columns_inserted = Signal()

    #: A signal which should be emitted when columns are removed. The
    #: payload should be the index of the removal and the number of
    #: columns removed.
    columns_removed = Signal()

    @abstractmethod
    def row_count(self):
        """ Get the number of rows in the model.

        Returns
        -------
        result : int
            The number of rows in the model.

        """
        raise NotImplementedError

    @abstractmethod
    def column_count(self):
        """ Get the number of columns in the model.

        Returns
        -------
        result : int
            The number of columns in the model.

        """
        raise NotImplementedError

    @abstractmethod
    def flags(self, row, column):
        """ Get the item flags for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : int
            An or'd combination of ItemFlag enum values for the given
            indices.

        """
        raise NotImplementedError

    @abstractmethod
    def data(self, row, column):
        """ Get the item data for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : object or None
            The data value for the given indices, or None if no data is
            available.

        """
        raise NotImplementedError

    def edit_data(self, row, column):
        """ Get the item edit data for the given indices.

        This is the data that will be displayed when an editor is
        opened for the given cell.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : object or None
            The edit data value for the given indices, or None if no
            edit data is available. The default implementation of this
            method returns the result of the `data` method.

        """
        return self.data(row, column)

    def icon_source(self, row, column):
        """ Get the icon source for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : str or None
            The source url for the item icon, or None if no icon is
            available. The default implementation of this method
            returns None.

        """
        return None

    def tool_tip(self, row, column):
        """ Get the tool tip for the given item indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : str or None
            The tool tip for the item, or None if no tool tip is
            available. The default implementation of this method
            returns None.

        """
        return None

    def status_tip(self, row, column):
        """ Get the status tip for the given item indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : str or None
            The status tip for the item, or None if no status tip is
            available. The default implementation of this method
            returns None.

        """
        return None

    def font(self, row, column):
        """ Get the font for the given item indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : str or None
            The font string for the item, or None if there is no font
            available. The font string should conform to the shorthand
            CSS3 font specification. The default implementation of this
            method returns None.

        """
        return None

    def background(self, row, column):
        """ Get the background color for the given item indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : str or None
            The background color string for the item, or None if there
            is no background color available. The color string should
            conform to the CSS3 color specification. The default
            implementation of this method returns None.

        """
        return None

    def foreground(self, row, column):
        """ Get the foreground color for the given item indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : str or None
            The foreground color string for the item, or None if there
            is no foreground color available. The color string should
            conform to the CSS3 color specification. The default
            implementation of this method returns None.

        """
        return None

    def text_alignment(self, row, column):
        """ Get the text alignment for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : int
            An or'd combination of AlignmentFlag enum values for the
            given indices. The default implementation of this method
            returns AlignmentFlag.ALIGN_CENTER.

        """
        return AlignmentFlag.ALIGN_CENTER

    def check_state(self, row, column):
        """ Get the check state for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : int or None
            One of the CheckState enum values, or None if the item has
            no check state. The default implementation of this method
            returns None.

        """
        return None

    def size_hint(self, row, column):
        """ Get the size hint for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        Returns
        -------
        result : tuple or None
            The (width, height) size hint for the item, or None if the
            item has no size hint. The default implementation of this
            method returns None.

        """
        return None

    def set_data(self, row, column, value):
        """ Set the item data for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        value : object
            The value entered by the user.

        Returns
        -------
        result : bool
            True if the item was set successfully, False otherwise. The
            default implementation of this method returns False.

        """
        return False

    def set_check_state(self, row, column, value):
        """ Set the check state for the given indices.

        Parameters
        ----------
        row : int
            The row index of the item.

        column : int
            The column index of the item.

        value : CheckState
            One of the CheckState enum values.

        Returns
        -------
        result : bool
            True if the item state set successfully, False otherwise.
            The default implementation of this method returns False.

        """
        return False


class NullItemModel(AbstractItemModel):
    """ A null implementation of AbstractItemModel.

    """
    def row_count(self):
        return 0

    def column_count(self):
        return 0

    def flags(self, row, column):
        return ItemFlag.NO_ITEM_FLAGS

    def data(self, row, column):
        return None


class AbstractTableModel(AbstractItemModel):
    """ A abstract class for defining item based table models.

    A table model adds explicit support for row and column headers.

    """
    @abstractmethod
    def row_header_data(self, index):
        """ Get the row header data for the given index and role.

        Parameters
        ----------
        index : int
            The row index for the header.

        Returns
        -------
        result : object or None
            The data value for the given index, or None if no data is
            available.

        """
        raise NotImplementedError

    @abstractmethod
    def column_header_data(self, index):
        """ Get the column header item for the given index.

        Parameters
        ----------
        index : int
            The column index for the header.

        Returns
        -------
        result : object or None
            The data value for the given index, or None if no data is
            available.

        """
        raise NotImplementedError


class NullTableModel(AbstractTableModel):
    """ A null implementation of AbstractTableModel.

    """
    def row_count(self):
        return 0

    def column_count(self):
        return 0

    def flags(self, row, column):
        return ItemFlag.NO_ITEM_FLAGS

    def data(self, row, column):
        return None

    def row_header_data(self, index):
        return None

    def column_header_data(self, index):
        return None

