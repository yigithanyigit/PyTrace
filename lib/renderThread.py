import time
import traceback
import os
from multiprocessing import Queue

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from lib.vector import Vector2f, Vector3f
from lib.renderer import RendererWidget


def render_task_wrapper(args):
    return render_task(*args)


def render_task(y0, y1, width, scene, camera, height):
    imgbuffer = [0, 0, 0] * (y1 - y0) * width
    try:
        print("Process started", y0, y1)
        idx = 0
        for y in range(y0, y1):
            for x in range(0, width):
                coord = Vector2f(x / width, y / height)
                coord = coord * 2 - Vector2f(1, 1)
                color = RendererWidget.perPixel(coord, scene, camera)
                idx1 = (y - y0) * width + x
                imgbuffer[idx] = color.x
                imgbuffer[idx + 1] = color.y
                imgbuffer[idx + 2] = color.z
                idx += 3
        print("Process finished", y0, y1)
        return (imgbuffer, y0, y1)
    except BrokenPipeError:
        print(f"BrokenPipeError caught in worker {os.getpid()}")
    except Exception as e:
        print(f"Exception in process for y0={y0}, y1={y1}: {e}")
        traceback.print_exc()


"""
class RenderSignal(QObject):
    finished = Signal(float)


class RenderTask(QRunnable):

    def __init__(self, rendererWidget, y0, y1, width, scene, camera, height ,parent=None):
        super(RenderTask, self).__init__(parent)
        self.rendererWidget = rendererWidget
        self.y0 = y0
        self.y1 = y1
        self.width = width
        self.scene = scene
        self.camera = camera
        self.height = height

        self.signal = RenderSignal()

    def run(self):
        print("Thread started", self.y0, self.y1)
        start = time.process_time()
        for y in range(self.y0, self.y1):
            for x in range(0, self.width):
                coord = Vector2f(x / self.width, y / self.height)
                coord = coord * 2 - Vector2f(1, 1)
                color = self.rendererWidget.perPixel(coord, self.scene, self.camera)
                self.rendererWidget.imgBuffer.setPixelColor(x, y, QColor(color.x, color.y, color.z))
        end = time.process_time()
        self.signal.finished.emit(end - start)


"""
"""
class RenderThread(QThread):
    rowRendered = Signal(int)

    def __init__(self, rendererWidget, y0, y1, width, scene, camera, height ,parent=None):
        super(RenderThread, self).__init__(parent)
        self.rendererWidget = rendererWidget
        self.y0 = y0
        self.y1 = y1
        self.width = width
        self.scene = scene
        self.camera = camera
        self.height = height

    def run(self):
        for y in range(self.y0, self.y1):
            for x in range(0, self.width):
                coord = Vector2f(x / self.width, y / self.height)
                coord = coord * 2 - Vector2f(1, 1)
                color = self.rendererWidget.perPixel(coord, self.scene, self.camera)
                self.rendererWidget.imgBuffer.setPixelColor(x, y, QColor(color.x, color.y, color.z))
        self.rowRendered.emit(y)
"""
