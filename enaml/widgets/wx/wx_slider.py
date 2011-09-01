# -*- coding: utf-8 -*-
import wx

from traits.api import (implements, Bool, Event, Str, Enum, Float, Any,
                        Range, Callable, TraitError)

from enaml.widgets.wx.wx_element import WXElement
from enaml.widgets.i_slider import ISlider
from enaml.enums import Orientation, TickPosition


class WXSlider(WXElement):
    """A simple slider widget.

    A slider can be used to select from a continuous range of values.
    The slider's range is fixed at 0.0 to 1.0. Therefore, the position
    of the slider can be viewed as a percentage. To facilitate various
    ranges, you can specify from_pos and to_pos callables to convert to
    and from the position the value.

    Attributes
    ----------
    down : Bool
        Whether or not the slider is pressed down.

    from_slider : Callable
        A function that takes one argument to convert from the slider
        postion to the appropriate Python value.

    to_slider : Callable
        A function that takes one argument to convert from a Python
        value to the appropriate slider position.

    slider_pos : Float
        The floating point percentage (0.0 - 1.0) which is the position
        of the slider. This value is always updated while the slider is
        moving.

    value : Any
        The value of the slider. This is set to the value of
        from_slider(slider_pos).

    tracking : Bool
        If True, the value is updated while sliding. Otherwise, it is
        only updated when the slider is released. Defaults to True.

    tick_interval : Float
        The slider_pos interval to put between tick marks. Default is `0.1`.

    tick_position : TickPosition Enum value
        A TickPosition enum value indicating how to display the tick
        marks.

    orientation : Orientation Enum value
        The orientation of the slider. One of the Orientation enum
        values.

    pressed : Event
        Fired when the slider is pressed.

    released : Event
        Fired when the slider is released.

    moved : Event
        Fired when the slider is moved.

    invalid_value: Event
        Fired when there was an attempt to assign an invalid (out of range)
        value to the slider.
    """

    implements(ISlider)

    #--------------------------------------------------------------------------
    # ISlider interface
    #--------------------------------------------------------------------------

    down = Bool

    from_slider = Callable(lambda pos: pos)

    to_slider = Callable(lambda val: val)

    slider_pos = Range(0.0, 1.0)

    value = Any

    tracking = Bool(True)

    tick_interval = Float(0.1)

    ticks = Enum(*TickPosition.values())

    orientation = Enum(*Orientation.values())

    pressed = Event

    released = Event

    moved = Event

    invalid_value = Event

    #==========================================================================
    # Implementation
    #==========================================================================

    def create_widget(self):
        """Initialization of ISlider based on wxWidget"""
        # create widget
        widget = wx.Slider(parent=self.parent_widget())

        # Bind class functions to wx widget events
        if wx.PlatformInfo[1] == 'wxMSW':
            widget.Bind(wx.EVT_SCROLL_CHANGED, self._on_slider_changed)
        widget.Bind(wx.EVT_SCROLL_THUMBRELEASE, self._on_thumb_release)
        widget.Bind(wx.EVT_SCROLL_THUMBTRACK, self._on_thumb_track)
        widget.Bind(wx.EVT_LEFT_DOWN, self._on_left_down)
        widget.Bind(wx.EVT_LEFT_UP, self._on_left_up)

        # associate widget
        self.widget = widget

    #--------------------------------------------------------------------------
    # Initialization
    #--------------------------------------------------------------------------

    def init_attributes(self):
        """initialize WXSlider attributes"""

        # down
        self.down = False

        minimum = self._convert_for_wx(0.0)
        maximum = self._convert_for_wx(1)
        self.widget.SetRange(minimum, maximum)

        # slider position
        self.value = self.from_slider(self.slider_pos)

        return

    def init_meta_handlers(self):
        """initialize WXSlider meta styles"""
        return

    #--------------------------------------------------------------------------
    # Private methods
    #--------------------------------------------------------------------------

    def _convert_for_wx(self, value):
        """Converts the value to an integer suitable for the wxSlider"""
        position = int(round(value / self.tick_interval))
        return position

    def _convert_from_wx(self, value):
        """Converts the value to an integer suitable for the wxSlider"""
        position = value * self.tick_interval
        return position

    def _thumb_hit(self, point):
        """Is the point in the thumb area"""

        # TODO: consider the slider orientation
        width = float(self.widget.GetSizeTuple()[0])

        # the relative size of the thumb
        thumb = self.widget.GetThumbLength() / width

        # the relative position of the point
        y = point[0] / width

        # minimum and maximum position (edges) of the thumb
        minimum = self.slider_pos - thumb
        maximum = self.slider_pos + thumb

        return minimum <= y <= maximum

    #--------------------------------------------------------------------------
    # Notification
    #--------------------------------------------------------------------------

    def _value_changed(self):
        """Update the slider position

        update the `slider_pos` to respond to the `value` change.

        .. note:: The assignment to the slider_pos might fail because 'value'
            is out of range. In that case the last known good value is given
            back to the value attribute.
        """
        # The try...except block is required because we need to keep the
        # `value` attribute in sync with the `slider_pos` and **valid**
        try:
            self.slider_pos = self.to_slider(self.value)
        except TraitError as ex:
            # revert value
            self.value = self.from_slider(self.slider_pos)
            self.invalid_value = ex
        return

    def _slider_pos_changed(self):
        """Update the position in the slider widget

        there are a lot of conversions taking place due to the three
        different variables (value, slider.pos, widget value) that need to
        be in sync.

        .. note:: The wx widget uses integers for the slider range. This
            requires to convert the decimal values in the `slider_pos`
            attribute to an integer.
        """

        # check and update the wxSlider
        position = self._convert_for_wx(self.slider_pos)
        if position != self.widget.GetValue():
            self.widget.SetValue(position)

        self.value = self.from_slider(self.slider_pos)
        self.moved = self.value
        return

    #--------------------------------------------------------------------------
    # Event handlers
    #--------------------------------------------------------------------------

    def _on_thumb_release(self, event):
        self.down = False
        if wx.PlatformInfo[1] != 'wxMSW':
            self._on_slider_changed(event)
        self.released = event
        event.Skip()
        return

    def _on_slider_changed(self, event):
        # comparing the values as integers is probably safer
        new_position = self.widget.GetValue()
        old_position = self._convert_for_wx(self.slider_pos)
        if new_position != old_position:
            self.slider_pos = self._convert_from_wx(new_position)
        event.Skip()
        return

    def _on_thumb_track(self, event):
        self.down = True
        if self.tracking:
            self._on_slider_changed(event)
        event.Skip()
        return

    def _on_left_down(self, event):
        """Check if the mouse was pressed over the thumb

        The function tries to estimate the position of the thumb and then
        checks if the mouse was pressed over it to fire the `pressed` event and
        set the `down` attribute.

        .. todo:: check with orientation
        """
        # TODO check orientation
        mouse_position = event.GetPosition()
        if self._thumb_hit(mouse_position):
            self.down = True
            self.pressed = event
        event.Skip()
        return

    def _on_left_up(self, event):
        if wx.PlatformInfo[1] != 'wxMSW':
            self._on_slider_changed(event)
        self.down = False
        event.Skip()

if __name__ == '__main__':
    """Test example of the WXSlider"""

    from cStringIO import StringIO

    from traits.api import HasTraits

    from enaml.factories.enaml_factory import EnamlFactory

    enaml = """
from traits.api import Float

Window main:
    title = "Slider demo"
    Panel:
        VGroup:
            Label:
                text << " value :{0} \\n slider_pos: {1} \\n down: {2}".\
                        format(slider.value, slider.slider_pos, slider.down)
            Slider slider:
                value = 0.5
                tick_interval = 0.1
                tracking := track.checked
                released >> print('the slider was released!', msg.new)
                pressed >> print('the slider was pressed!', msg.new)
                moved >> print('the slider has moved!', msg.new)
                invalid_value >> print('the value was invalid!', msg.new)
            HGroup:
                PushButton:
                    text = "Adjust by +0.1"
                    clicked >> model.update(slider, 0.1)
                PushButton:
                    text = "Adjust by -0.1"
                    clicked >> model.update(slider, -0.1)
                CheckBox track:
                    text = "Track"

"""

    class Model(HasTraits):
        window_title = Str('Slider')

        def update(self, slider, offset):
            slider.value += offset
            return

    fact = EnamlFactory(StringIO(enaml))
    app = wx.App()
    view = fact(model=Model())
    view.show()
    app.MainLoop()
