from gi.repository import Clutter, GLib
from random import randint

try:
    from IPython.lib.inputhook import InputHookBase, inputhook_manager
    import sys
    GUI_CLUTTER = 'gui_clutter'

    def _main_quit(*_):
        Clutter.main_quit()
        return False

    def inputhook_clutter():
        # end the running mainloop when input is available on stdin
        GLib.io_add_watch(sys.stdin, GLib.IO_IN, _main_quit)
        # start the main loop
        Clutter.main()
        return 0

    @inputhook_manager.register('clutter')
    class ClutterInputHook(InputHookBase):

        def enable(self, app=None):
            """Enable event loop integration with Clutter.

            Parameters
            ----------
            app : ignored
               Ignored, it's only a placeholder to keep the call signature of all
               gui activation methods consistent, which simplifies the logic of
               supporting magics.

            Notes
            -----
            This methods sets the PyOS_InputHook for Clutter, which allows
            Clutter to integrate with terminal based applications like IPython.
            """
            if GUI_CLUTTER not in self.manager.apps:
                Clutter.init([])

            self.manager.set_inputhook(inputhook_clutter)
            self.manager._current_gui = GUI_CLUTTER
            self.manager.apps[GUI_CLUTTER] = True

except ImportError:
    pass


class Example(object):

    def __init__(self):
        self.stage = Clutter.Stage()
        self.stage.set_title('Clutter example')
        self.stage.set_background_color(Clutter.color_from_string('#BBB')[1])
        self.stage.set_size(300.0, 300.0)

        self.actor = Clutter.Actor()
        self.actor.set_background_color(Clutter.color_from_string('#DA0060')[1])
        self.actor.set_position(75.0, 75.0)
        self.actor.set_size(150.0, 150.0)
        self.actor.set_pivot_point(0.5, 0.5)

        self.rotation = Clutter.PropertyTransition(property_name='rotation-angle-z')
        self.rotation.set_animatable(self.actor)
        self.rotation.set_duration(5000)
        self.rotation.set_from(0.0)
        self.rotation.set_to(360.0)
        self.rotation.set_repeat_count(-1)
        self.rotation.start()

        self.stage.add_child(self.actor)
        self.stage.show()
        self.actor.set_reactive(True)

        self.actor.connect('button-press-event', self.color_actor)
        self.stage.connect('key-press-event', self.on_key_press)
        self.stage.connect('destroy', lambda *_: Clutter.main_quit())

    def on_key_press(self, target, event):
        if event.keyval == Clutter.Escape:
            Clutter.main_quit()

    def color_actor(self, *_):
        rgba = [randint(0, 255) for x in range(3)] + [255]
        print(rgba)
        self.actor.set_background_color(Clutter.Color.new(*rgba))

if __name__ == '__main__':
    Clutter.init([])
    example = Example()
    Clutter.main()
