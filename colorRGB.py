# CENG488 Assignment6 by
# Can Yavuzkurt
# 240201040
# May 2021

class ColorRGB(object):
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

    def __mul__(self, other):
        return ColorRGB(self.r * other, self.g * other, self.b * other)