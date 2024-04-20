import math
import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from lib.vector import Vector3f
from lib.scene import Objects_Enum

__all__ = ["RendererWidget"]


class RendererWidget(QWidget):
    def __init__(self, width, height, parent=None):
        super(RendererWidget, self).__init__(parent=parent)
        self.width = width
        self.height = height

        self._min_hit_point = sys.float_info.max
        self._closest_object = None

        # setup an image buffer
        self.imgBuffer = QImage(
            self.width, self.height, QImage.Format_ARGB32_Premultiplied
        )
        self.imgBuffer.fill(QColor(0, 0, 0))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.drawImage(0, 0, self.imgBuffer)

    def sizeHint(self):
        return QSize(self.width, self.height)

    @staticmethod
    def sphereIntersect(coord, sphere, camera, min_hit_point, closest_object):
        rayOrigin = Vector3f(camera[0], camera[1], camera[2])
        rayDirection = Vector3f(coord.x, coord.y, -1.0)
        radius = sphere[1]
        center = Vector3f(sphere[2], sphere[3], sphere[4])

        origin = rayOrigin - center
        a = Vector3f.dot(rayDirection, rayDirection)
        b = 2.0 * Vector3f.dot(origin, rayDirection)
        c = Vector3f.dot(origin, origin) - radius * radius
        discriminant = b * b - 4 * a * c

        if discriminant < 0:
            return (None, min_hit_point)
        closestT = (-b - math.sqrt(discriminant)) / (2.0 * a)
        if closestT < min_hit_point:
            return (sphere, closestT)
        return (None, min_hit_point)

    @staticmethod
    def perPixel(coord, scene, camera):
        if len(scene) == 0:
            return Vector3f(0, 0, 0)
        _min_hit_point = sys.float_info.max
        _closest_object = None
        idx = 0
        color = Vector3f(0, 0, 0)

        light_dir = []
        light_point = [] # TODO write proper code for lights

        while idx < len(scene):
            window_start = idx
            window_end = idx + scene[idx] + 1
            obj = scene[window_start + 1 : window_end]
            if obj[0] == Objects_Enum.SPHERE:
                res = RendererWidget.sphereIntersect(
                    coord, obj, camera, _min_hit_point, _closest_object
                )
                if res[0] is not None:
                    _closest_object = res[0]
                    _min_hit_point = res[1]
            if obj[0] == Objects_Enum.AMBIENT_LIGHT:
                color = Vector3f(min(255, color.x + obj[1]), min(255, color.y + obj[2]), min(255, color.z + obj[3]))
            if obj[0] == Objects_Enum.DIRECTIONAL_LIGHT:
                light_dir.append(obj)
            if obj[0] == Objects_Enum.POINT_LIGHT:
                light_point.append(obj)
            idx = window_end
        if _closest_object is None:
            return color

        # Calculate Directional Light
        if len(light_dir) > 0:
            for light in light_dir:
                light_dir = Vector3f(light[1], light[2], light[3])
                light_dir = light_dir.normalize()
                normal = Vector3f(coord.x, coord.y, _closest_object[4])
                normal = normal.normalize()
                dot = Vector3f.dot(normal, light_dir)
                if dot > 0:
                    color = Vector3f(min(255, color.x + dot * _closest_object[5]), min(255, color.y + dot * _closest_object[6]), min(255, color.z + dot * _closest_object[7]))
        #return Vector3f(min(255, color.x + _closest_object[5]), min(255, color.y + _closest_object[6]), min(255, color.z + _closest_object[7]))
        return color
