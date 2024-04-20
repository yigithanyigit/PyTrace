import sys
import random
import time
import os
from multiprocessing import Pool
import cProfile
from cProfile import Profile

from lib.renderer import RendererWidget
from lib.sceneParser import SceneParser
from lib.scene import Scene
from lib.procedural import Procedural
from lib.renderEvent import RenderEvent, RenderEventHandler
from lib.camera import Camera
from lib.renderThread import render_task, render_task_wrapper
from lib.argumentParser import ArgumentParser

os.environ["QT_MAC_WANTS_LAYER"] = "1"

SCENE_FILE = "scene_procedural.json"

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import time


class PyTraceMainWindow(QMainWindow):
    def __init__(self, qApp, width, height, scene, camera):
        super(PyTraceMainWindow, self).__init__()

        self.qApp = qApp
        self.width = width
        self.height = height
        self.gfxScene = QGraphicsScene()
        self.definedScene = scene
        self.camera = camera
        self.cumulativeTime = 0.0

    def setupUi(self):
        if not self.objectName():
            self.setObjectName("PyTrace")
            self.resize(self.width + int(25), self.height + int(25))
            self.setWindowTitle("CENG488 PyTrace")
            self.setStyleSheet("background-color:black;")
            self.setAutoFillBackground(True)

        # set centralWidget
        self.centralWidget = QWidget(self)
        self.centralWidget.setObjectName("CentralWidget")

        # create a layout to hold widgets
        self.horizontalLayout = QHBoxLayout(self.centralWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        # setup the gfxScene
        self.gfxScene.setItemIndexMethod(QGraphicsScene.NoIndex)

        # create a paint widget
        self.rendererWidget = RendererWidget(self.width, self.height)
        self.rendererWidget.setGeometry(QRect(0, 0, self.width, self.height))
        self.rendererWidgetItem = self.gfxScene.addWidget(self.rendererWidget)
        self.rendererWidgetItem.setZValue(0)

        # create a QGraphicsView as the main widget
        self.gfxView = QGraphicsView(self.centralWidget)
        self.gfxView.setObjectName("GraphicsView")

        # assign our scene to view
        self.gfxView.setScene(self.gfxScene)
        self.gfxView.setGeometry(QRect(0, 0, self.width, self.height))

        # add widget to layout
        self.horizontalLayout.addWidget(self.gfxView)

        # set central widget
        self.setCentralWidget(self.centralWidget)

        # setup a status bar
        self.statusBar = QStatusBar(self)
        self.statusBar.setObjectName("StatusBar")
        self.statusBar.setStyleSheet("background-color:gray;")
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Ready...")

    def setStatusBarMessage(self, message):
        self.statusBar.showMessage(message)

    def timerBuffer(self):
        """
        print("Updating buffer...")
        self.setStatusBarMessage("Rendering...")

        self.threadPool = QThreadPool().globalInstance()
        max_thread = os.cpu_count()
        self.threadPool.setMaxThreadCount(max_thread)
        height_per_thread = self.height // max_thread

        for bucket in range(0, height_per_thread):
            for i in range(0, max_thread):
                y0 = bucket * max_thread + i
                y1 = y0 + 1
        """
        """
        for i in range(0, max_thread):
            y0 = i * height_per_thread
            y1 = y0 + height_per_thread
            if i == max_thread - 1:
                y1 = self.height
            thread = RenderTask(self.rendererWidget, y0, y1, self.width, self.definedScene, camera, self.height)
            thread.signal.finished.connect(self.updateBuffer)
            self.threadPool.start(thread)

            while not self.threadPool.waitForDone(100): # This is a must for process the signals, otherwise the GUI will freeze
                qApp.processEvents()

        self.printCumulativeTime(self.cumulativeTime)
        """
        start = time.time()
        max_thread = os.cpu_count()
        height_per_thread = self.height // max_thread
        camera_shared = [0, 0, 0, 0]
        scene_shared = scene.getSharedArray()
        camera_shared[0] = self.camera.posX
        camera_shared[1] = self.camera.posY
        camera_shared[2] = self.camera.posZ
        camera_shared[3] = self.camera.focalLength
        with Pool(processes=max_thread) as pool:
            self.setStatusBarMessage(
                "Rendering... | Using " + str(max_thread) + " workers"
            )
            self.updateBuffer()
            arg_list = []
            for i in range(0, max_thread):
                y0 = i * height_per_thread
                y1 = y0 + height_per_thread
                if i == max_thread - 1:
                    y1 = self.height
                args = (y0, y1, self.width, scene_shared, camera_shared, self.height)
                arg_list.append(args)
            for res in pool.imap(render_task_wrapper, arg_list):
                # TODO Implement a timer function to handle interrups
                print("Updating Buffer...")
                result = res[0]
                idx = 0
                for y in range(res[1], res[2]):
                    y = y - res[1]
                    for x in range(0, self.width):
                        self.rendererWidget.imgBuffer.setPixelColor(
                            x,
                            y + res[1],
                            QColor(
                                result[idx],
                                result[idx + 1],
                                result[idx + 2],
                            ),
                        )
                        idx += 3
                    self.updateBuffer()
        end = time.time()
        self.printCumulativeTime(end - start)

    def updateBuffer(self):
        self.rendererWidget.update()
        qApp.processEvents()

    def printCumulativeTime(self, time):
        print("Cumulative time: ", time)
        self.setStatusBarMessage(
            "Ready... | Last Render Time: " + str(time) + " seconds"
        )

if __name__ == "__main__":
    # setup a QApplication
    qApp = QApplication(sys.argv)
    qApp.setOrganizationName("CENG488")
    qApp.setOrganizationDomain("cavevfx.com")
    qApp.setApplicationName("PyTrace")
    print("PyTrace is starting...")

    # setup parser
    parser = ArgumentParser(sys.argv)

    # setup a scene
    sceneParser = SceneParser(parser.args.scene)
    sceneParser.parseScene()
    scene = Scene()
    camera = Camera(
        sceneParser.camera["posX"],
        sceneParser.camera["posY"],
        sceneParser.camera["posZ"],
        sceneParser.camera["focalLength"],
    )

    if sceneParser.procedural is not None:
        for obj in sceneParser.procedural.objects:
            scene.addNode(obj)

    if sceneParser.objects is not None:
        for obj in sceneParser.objects:
            scene.addNode(obj)

    if sceneParser.lights is not None:
        for obj in sceneParser.lights:
            scene.addNode(obj)

    # setup main ui
    width = parser.args.width
    height = parser.args.height
    mainWindow = PyTraceMainWindow(qApp, width, height, scene, camera)
    mainWindow.setupUi()
    mainWindow.show()

    # Create a render event and handler
    renderEvent = RenderEvent()
    renderEventHandler = RenderEventHandler(mainWindow)

    # Handle the render event whenever the camera changes
    camera.cameraMovedSignal.connect(
        lambda: qApp.postEvent(renderEventHandler, renderEvent)
    )

    # Start rendering when the application starts
    QTimer.singleShot(0, lambda: qApp.postEvent(renderEventHandler, renderEvent))

    # enter event loop
    sys.exit(qApp.exec_())
