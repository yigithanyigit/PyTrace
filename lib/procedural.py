import random

from lib.vector import Vector3f
from lib.objects_enum import Objects_Enum

class Procedural:
    def __init__(self, upperleft, bottomright, noofspheres, radiusLo, radiusHi):
        self.upperleft = Vector3f(upperleft['x'], upperleft['y'], upperleft['z'])
        self.bottomright = Vector3f(bottomright['x'], bottomright['y'], bottomright['z'])
        self.noofspheres = int(noofspheres)
        self.radiusLo = float(radiusLo)
        self.radiusHi = float(radiusHi)
        self.objects = []

    def generateSpheres(self):
        # Generate spheres procedurally
        spheres = []
        for i in range(self.noofspheres):
            x = random.uniform(self.upperleft.x, self.bottomright.x)
            y = random.uniform(self.upperleft.y, self.bottomright.y)
            z = random.uniform(self.upperleft.z, self.bottomright.z)
            radius = random.uniform(self.radiusLo, self.radiusHi)
            spheres.append({"type": Objects_Enum.SPHERE, "radius": radius, "posX": x, "posY": y, "posZ": z, "color": {"r": random.uniform(0, 255), "g": random.uniform(0, 255), "b": random.uniform(0, 255)}})
        self.objects = spheres