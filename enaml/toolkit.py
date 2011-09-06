import os

from traits.api import HasStrictTraits, Dict, Str, Callable, Any

from .constructors import IToolkitConstructor
from .util.trait_types import SubClass


class Toolkit(HasStrictTraits):
    """ A simple class that handles toolkit related functionality.

    Attributes
    ----------
    items : Dict(Str, SubClass(IToolkitConstructor))
        A dictionary which maps type names in the Enaml source code
        to toolkit constructor classes for that name. This dict
        can be modified to make new widgets available to the Enaml
        source code.

    prime : Callable
        A callable which initializes the toolkit's event loop. This
        will be called before any toolkit widgets are created. Most
        toolkits will create the application object in this function.
        The return value of this callable is passed to the 'start'
        callable when the event loop should be started.

    start : Callable
        This is called at the end of the ui building process, after
        the 'show' method on the view has been called. This function
        should make sure the event loop for the toolkit is started.
        It should take one argument, which is the return value from
        the 'prime' method.

    app : Any
        The return value of the 'prime' callable is stored in this
        attribute. This will usually be the toolkit's application
        object.

    Methods
    -------
    create_ctor(name):
        Creates the constructor instance for the given name, or raises
        an error if no constructor is defined for that name.

    prime_event_loop()
        Called before any ui tree building takes place in order to 
        prime the toolkit's event loop.

    start_event_loop()
        Called at the end of the View's 'show' method to start the 
        toolkit's event loop.

    """
    items = Dict(Str, SubClass(IToolkitConstructor))

    prime = Callable

    start = Callable

    app = Any

    def __init__(self, items, prime, start):
        super(Toolkit, self).__init__(items=items, prime=prime, start=start)

    def create_ctor(self, name):
        """ Creates the constructor instance for the given name, or 
        raises an error if no constructor is defined for that name.

        """
        try:
            ctor_cls = self.items[name]
        except KeyError:
            msg = 'Toolkit does not support the %s item.' % name
            raise ValueError(msg)
        return ctor_cls()
    
    def prime_event_loop(self):
        """ Called before any ui tree building takes place in order to 
        prime the toolkit's event loop. 
        
        """
        self.app = self.prime()
    
    def start_event_loop(self):
        """ Called at the end of the View's 'show' method to start the 
        toolkit's event loop.
        
        """
        self.start(self.app)


def default_toolkit():
    """ Creates an returns the default toolkit object based on
    the user's current ETS_TOOLKIT environment variables.

    """
    toolkit = os.environ.get('ETS_TOOLKIT', 'wx').lower()
    
    if toolkit == 'wx':
        return wx_toolkit()
        
    if toolkit == 'qt' or toolkit == 'qt4':
        qt_api = os.environ.get('QT_API', 'pyside').lower()
        
        if qt_api == 'pyside':
            return pyside_toolkit()
        
        if qt_api == 'pyqt' or qt_api == 'pyqt4':
            return pyqt_toolkit()
        
        raise ValueError('Invalid QT_API: %s' % qt_api)
    
    raise ValueError('Invalid Toolkit: %s' % toolkit)


def wx_toolkit():
    """ Creates and return a toolkit object for the wx backend.

    """
    from .widgets.wx import constructors as ctors
    
    items = {
        'Panel': ctors.WXPanelCtor,
        'Window': ctors.WXWindowCtor,
        'Dialog': ctors.WXDialogCtor,
        'Form': ctors.WXFormCtor,
        'Group': ctors.WXGroupCtor,
        'VGroup': ctors.WXVGroupCtor,
        'HGroup': ctors.WXHGroupCtor,
        'StackedGroup': ctors.WXStackedGroupCtor,
        'TabGroup': ctors.WXTabGroupCtor,
        'GroupBox': ctors.WXGroupBoxCtor,
        'Calendar': ctors.WXCalendarCtor,
        'CheckBox': ctors.WXCheckBoxCtor,
        'ComboBox': ctors.WXComboBoxCtor,
        'Field': ctors.WXFieldCtor,
        'Html': ctors.WXHtmlCtor,
        'Image': ctors.WXImageCtor,
        'Label': ctors.WXLabelCtor,
        'LineEdit': ctors.WXLineEditCtor,
        'PushButton': ctors.WXPushButtonCtor,
        'RadioButton': ctors.WXRadioButtonCtor,
        'Slider': ctors.WXSliderCtor,
        'SpinBox': ctors.WXSpinBoxCtor,
    }

    def prime_loop():
        import wx
        app = wx.GetApp()
        if app is None:
            app = wx.PySimpleApp()
        return app

    def start_loop(app):
        if not app.IsMainLoopRunning():
            app.MainLoop()

    return Toolkit(items=items, prime=prime_loop, start=start_loop)


def pyside_toolkit():
    raise NotImplementedError


def pyqt_toolkit():
    raise NotImplementedError

