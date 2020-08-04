from tkinter import Canvas
from PIL import Image as img, ImageTk as imgTk
from resources.colors import *
from views.prefabs.guiactivity import GUIActivity
from views.prefabs.abstract.guicontainer import GUIContainer
from models.bpmn.subprocess import SubProcess, ActivityFlag
from models.bpmndi.shape import BPMNShape

class GUISubProcess(GUIActivity, GUIContainer):

    TEXT_OFFSET_Y = 16

    def __init__(self, **args):
        GUIContainer.__init__(self, **args)
        GUIActivity.__init__(self, **args)

        self.element = args.get('element', SubProcess())

        # default size
        self.WIDTH = 250
        self.HEIGHT = 200

    def draw_at(self, x, y):
        # draw the border
        GUIActivity.draw_at(self, x, y)
        # draw collapsed subprocess icon
        iconpath = 'resources/icons/notation/collapsedsubprocess.png'
        self.type_icon = imgTk.PhotoImage(img.open(iconpath).resize((self.ICON_SIZE, self.ICON_SIZE)))
        cnv: Canvas = self.canvas
        self.id.append (cnv.create_image(x + (self.WIDTH / 2) + (self.ICON_MARGIN / 4) + (self.ICON_SIZE / 2), y + self.HEIGHT - self.ICON_MARGIN, image=self.type_icon))
        # draw text
        self.draw_text(self.element.name, x + self.WIDTH/2, y - self.TEXT_OFFSET_Y)

    def append_child(self, child):
        # prevention condition
        if child.__class__.__name__ == 'GUIProcess':
            return
        # continue, there are no problems
        super().append_child(child)