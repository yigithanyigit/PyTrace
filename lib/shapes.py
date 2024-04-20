from objParser import objParser
from boundingbox import *

__all__ = ['polyShape']


class polyShape:
	def __init__(self, name, vertices, faces):
		self.name = name
		self.vertices = vertices
		self.edges = []
		self.faces = faces
		self.colors = []
		self.obj2World = Matrix()
		self.bboxObj = BoundingBox()
		self.bboxWorld = BoundingBox()
		self.calcBboxObj()
		self.normals = None


	def calcBboxObj(self):
		for vertex in self.vertices:
			self.bboxObj.expand(vertex)

 
	@staticmethod
	def parseObjFile(name, file):
		objects = []
		elem = objParser(file)
		for obj in elem.objects:
			vertices = []
			for v in obj[0]:
				vertices.append(Point3f(v[0], v[1], v[2]))
			object = polyShape(obj[2], vertices, obj[1])
			objects.append(object)
		return objects
