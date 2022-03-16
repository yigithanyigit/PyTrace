class objParser:
	def __init__(self, obj):
		self.tempObj = []
		self.objects=[]

		if obj is "" or obj is None:
			return

		string = open(obj, 'r').read()
		self.objs = string.split("g default")

		for i in range(1,len(self.objs)):
			for obj in self.objs[i].split('\n'):
				if obj != "":
					self.tempObj.append(obj)
			self.objs[i] = self.tempObj
			self.tempObj=[]

		lenght = 0
		count = 0
		for obj in self.objs:
			vertices = []
			edges=[]
			objName = ""
			for elem in obj:
				line = elem.split(" ")
				if line[0] == "v":
					count += 1
					vertices.append(map(float , line[1:]))
				elif line[0] == "f":
					edges.append(map(lambda x: x -lenght -1, map(int, line[1:])))
				elif line[0] == "g":
					objName = line[1]
			lenght = count
			self.objects.append((vertices,edges,objName))
		self.objects=self.objects[1:]

