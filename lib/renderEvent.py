from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import cProfile


# Create a custom event for rendering
class RenderEvent(QEvent):
    def __init__(self):
        super(RenderEvent, self).__init__(QEvent.User)


# Create a custom event handler
class RenderEventHandler(QObject):
    def __init__(self, mainWindow):
        super(RenderEventHandler, self).__init__()
        self.mainWindow = mainWindow

    def event(self, event):
        if event.type() == QEvent.User:
            self.mainWindow.timerBuffer()
            # cProfile.runctx('self.mainWindow.timerBuffer()', globals(), locals(), filename="profile.prof")

            return True
        return super(RenderEventHandler, self).event(event)
