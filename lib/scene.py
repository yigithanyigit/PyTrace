from multiprocessing import Array

from lib.objects_enum import Objects_Enum

class Scene:
    def __init__(self):
        super(Scene, self).__init__()
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)

    def getSharedArray(self):
        """
        # Object Enum : Sphere 1
        # Radius
        # Position.X
        # Position.Y
        # Position.Z
        # Color.R
        # Color.G
        # Color.B
        """
        temp = []
        for i in range(0, len(self.nodes)):
            objs = []
            node = self.nodes[i]
            self._dfs(node, objs, 0)
            for j in range(0, len(objs)):
                temp.append(objs[j])
        return temp

    def _dfs(self, node, temp, level):
        if level == 0:
            temp.append(len(node))
        for e in node:
            if isinstance(node[e], dict):
                temp[0] += len(node[e]) - 1
                self._dfs(node[e], temp, level + 1)
            else:
                temp.append(node[e])




