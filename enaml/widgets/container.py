#------------------------------------------------------------------------------
#  Copyright (c) 2013, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from atom.api import (
    Bool, Constant, Coerced, CachedProperty, List, observe, set_default
)

from enaml.core.declarative import d_properties
from enaml.layout.geometry import Box
from enaml.layout.layout_helpers import vbox

from .constraints_widget import ConstraintsWidget, ConstraintMember


@d_properties('share_layout', 'padding')
class Container(ConstraintsWidget):
    """ A ConstraintsWidget subclass that provides functionality for
    laying out constrainable children according to their system of
    constraints.

    The Container is the canonical component used to arrange child
    widgets using constraints-based layout. Given a heierarchy of
    components, the top-most Container will be charged with the actual
    layout of the decendents. This allows constraints to cross the
    boundaries of Containers, enabling powerful and flexible layouts.

    There are widgets whose boundaries constraints may not cross. Some
    examples of these would be a ScrollArea or a TabGroup. See the
    documentation of a given container component as to whether or not
    constraints may cross its boundaries.

    """
    #: A boolean which indicates whether or not to allow the layout
    #: ownership of this container to be transferred to an ancestor.
    #: This is False by default, which means that every container
    #: get its own layout solver. This improves speed and reduces
    #: memory use (by keeping a solver's internal tableaux small)
    #: but at the cost of not being able to share constraints
    #: across Container boundaries. This flag must be explicitly
    #: marked as True to enable sharing.
    share_layout = Bool(False)

    #: A constant symbolic object that represents the internal left
    #: boundary of the content area of the container.
    contents_left = ConstraintMember()

    #: A constant symbolic object that represents the internal right
    #: boundary of the content area of the container.
    contents_right = ConstraintMember()

    #: A constant symbolic object that represents the internal top
    #: boundary of the content area of the container.
    contents_top = ConstraintMember()

    #: A constant symbolic object that represents the internal bottom
    #: boundary of the content area of the container.
    contents_bottom = ConstraintMember()

    #: A constant symbolic object that represents the internal width of
    #: the content area of the container.
    contents_width = Constant()

    def _default_contents_width(self):
        return self.contents_right - self.contents_left

    #: A constant symbolic object that represents the internal height of
    #: the content area of the container.
    contents_height = Constant()

    def _default_contents_height(self):
        return self.contents_bottom - self.contents_top

    #: A constant symbolic object that represents the internal center
    #: along the vertical direction the content area of the container.
    contents_v_center = Constant()

    def _default_contents_v_center(self):
        return self.contents_top + self.contents_height / 2.0

    #: A constant symbolic object that represents the internal center
    #: along the horizontal direction of the content area of the container.
    contents_h_center = Constant()

    def _default_contents_h_center(self):
        return self.contents_left + self.contents_width / 2.0

    #: A box object which holds the padding for this component. The
    #: padding is the amount of space between the outer boundary box
    #: and the content box. The default padding is (10, 10, 10, 10).
    #: Certain subclasses, such as GroupBox, may provide additional
    #: margin than what is specified by the padding.
    padding = Coerced(Box, factory=lambda: Box(10, 10, 10, 10))

    #: A cached property which returns the children defined on the
    #: container which are instances of ConstraintsWidget.
    widgets = CachedProperty(List())

    #: Containers freely exapnd in width and height. The size hint
    #: constraints for a Container are used when the container is
    #: not sharing its layout. In these cases, expansion of the
    #: container is typically desired.
    hug_width = set_default('ignore')
    hug_height = set_default('ignore')

    #--------------------------------------------------------------------------
    # Property Handlers
    #--------------------------------------------------------------------------
    def _get_widgets(self):
        """ The getter for the 'widgets' cached property

        """
        isinst = isinstance
        target = ConstraintsWidget
        return [child for child in self.children if isinst(child, target)]

    #--------------------------------------------------------------------------
    # Widget Updates
    #--------------------------------------------------------------------------
    @observe(r'^(share_layout|padding)$', regex=True)
    def _layout_invalidated(self, change):
        """ A private observer which invalidates the layout.

        """
        # The superclass handler is sufficient.
        super(Container, self)._layout_invalidated(change)

    #--------------------------------------------------------------------------
    # Child Events
    #--------------------------------------------------------------------------
    def child_added(self, child):
        """ Handle the child added event on the container.

        This event handler will send a relayout event if the `Container`
        is active and the user has not defined their own constraints.

        """
        super(Container, self).child_added(child)
        # XXX these can probably be collapsed
        CachedProperty.reset(self, 'widgets')
        if self.is_active and not self.constraints:
            self._send_relayout()

    def child_removed(self, child):
        """ Handle the child removed event on the container.

        This event handler will send a relayout event if the `Container`
        is active and the user has not defined their own constraints.

        """
        super(Container, self).child_removed(child)
        # XXX these can probably be collapsed
        CachedProperty.reset(self, 'widgets')
        if self.is_active and not self.constraints:
            self._send_relayout()

    #--------------------------------------------------------------------------
    # Constraints Generation
    #--------------------------------------------------------------------------
    def _layout_info(self):
        """ An overridden parent class method which adds the 'share'
        layout key to the dict of layout information sent to the client.

        """
        layout = super(Container, self)._layout_info()
        layout['share_layout'] = self.share_layout
        layout['padding'] = self.padding
        return layout

    def _get_default_constraints(self):
        """ Supplies a default vbox constraint to the constraints
        children of the container if other constraints are not given.

        """
        cns = super(Container, self)._get_default_constraints()
        cns.append(vbox(*self.widgets))
        return cns

