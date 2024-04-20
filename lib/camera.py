from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

class Camera(QObject):
    
    cameraMovedSignal = Signal()
    
    def __init__(self, posX, posY, posZ, focalLength):
        super(Camera, self).__init__()
        self.posX = posX
        self.posY = posY
        self.posZ = posZ
        self.focalLength = focalLength
        
    def __repr__(self):
        return "Camera at position: " + str(self.posX) + " " + str(self.posY) + " " + str(self.posZ) + " with focal length: " + str(self.focalLength)
    
    def cameraMoved(self):
        self.cameraMovedSignal.emit(self.camera)