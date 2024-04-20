import json

from lib.procedural import Procedural
from lib.objects_enum import Objects_Enum

OBJECTS = ['spheres', 'cubes']


class SceneParser:
    # A class parser that parses scene.json file
    # Attrubutes:
    #   renderSettings: dict{xres, yres, samples}
    #   camera: dict{posX, posY, posZ, focalLength}
    #   objects: list[dict{radius, posX, posY, posZ, color{red, green, blue}}]
    # procedural:
    #  upperleft: dict{x, y, z}
    #  bottomright: dict{x, y, z}
    #  noofspheres: int
    #  radiusLo: float
    #  radiusHi: float
    def __init__(self, sceneFile):
        self.sceneFile = sceneFile
        self.renderSettings = {}
        self.camera = {}
        self.procedural = None
        self.lights = []
        self.objects = []

    def parseScene(self):
        # Parse the scene.json file
        with open(self.sceneFile) as f:
            scene = json.load(f)
            try:
                self.renderSettings = scene["renderSettings"]
            except KeyError:
                print("No render settings found in scene.json")
            try:
                self.camera = scene["camera"]
            except KeyError:
                print("No camera settings found in scene.json")
            try:
                for light in scene["lightSources"]:
                    if light['type'] == 'directional':
                        light['type'] = Objects_Enum.DIRECTIONAL_LIGHT
                    elif light['type'] == 'point':
                        light['type'] = Objects_Enum.POINT_LIGHT
                    elif light['type'] == 'spot':
                        light['type'] = Objects_Enum.SPOT_LIGHT
                    elif light['type'] == 'ambient':
                        light['type'] = Objects_Enum.AMBIENT_LIGHT
                    self.lights.append(light)
            except KeyError:
                print("No light settings found in scene.json")
            try:
                self.procedural = Procedural(
                    scene["procedural"]["upperLeft"],
                    scene["procedural"]["bottomRight"],
                    scene["procedural"]["nofSpheres"],
                    scene["procedural"]["radiusLo"],
                    scene["procedural"]["radiusHi"],
                )
                self.procedural.generateSpheres()
            except KeyError:
                print("No procedural settings found in scene.json")
            for obj_type in OBJECTS:
                try:
                    for obj in scene[obj_type]:
                        if obj_type == 'spheres':
                            obj['type'] = Objects_Enum.SPHERE
                        elif obj_type == 'cubes':
                            obj['type'] = Objects_Enum.CUBE
                        ordered_dict = {'type': obj['type']}
                        ordered_dict.update({k: v for k, v in obj.items() if k != 'type'})
                        self.objects.append(ordered_dict)
                except KeyError:
                    pass

