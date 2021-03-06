from tkinter import *
from views.components.icon import IconFrame
from resources.colors import *
from views.effects.animatable import Animatable
from views.effects.color_transition import ColorTransition

class TextBox(Frame, Animatable):

    def __init__(self, master, iconPath, **args):
        Frame.__init__(self, master, **args)

        self.configure(bg=black, pady=3)

        self.icon = IconFrame(self, iconPath, 15, black, 40, bg=black)
        self.icon.pack(side=LEFT)

        self.entry = Entry(self, relief=FLAT, font='-size 12 -weight bold', bd=5, fg=black)
        self.entry.pack(side=LEFT, fill=BOTH, expand=1, padx=(0, 3))

        Animatable.__init__(self)

    def get_text(self):
        return str(self.entry.get()).lstrip(' ').rstrip(' ')

    def clear(self):
        self.entry.delete(0, len(self.entry.get()))

    def bind_events(self):
        self.entry.bind('<FocusIn>', lambda e: self.onEnter())
        self.entry.bind('<FocusOut>', lambda e: self.onLeave())

    def changeFocusColor(self, color):
        self.stop_transitions()

        def _set (v): self['bg'] = v
        _get = lambda: self['bg']
        
        def _set1 (v): self.icon['bg'] = v
        _get1 = lambda: self.icon['bg']
        
        def _set2 (v): self.entry['fg'] = v
        _get2 = lambda: self.entry['fg']

        self.icon.set_bgColor(color)
        self.save_transition(ColorTransition(_set, _get, color))
        self.save_transition(ColorTransition(_set1, _get1, color))
        self.save_transition(ColorTransition(_set2, _get2, color))

    def onEnter(self):
        self.changeFocusColor(teal)

    def onLeave(self):
        self.changeFocusColor(black)