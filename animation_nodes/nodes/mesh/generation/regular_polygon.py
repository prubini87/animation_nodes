import bpy
import math
from bpy.props import *
from .... base_types import AnimationNode
#from .... algorithms.mesh_generation.regular_polygon import getRegularPolygonMesh, getRegularPolygonsMesh
from .... data_structures import (
    Mesh,
    Vector3DList,
    EdgeIndicesList,
    PolygonIndicesList
)

class RegularPolygonNode(bpy.types.Node, AnimationNode):
    bl_idname = "an_RegularPolygonNode"
    bl_label = "Regular Polygon Mesh"
    errorHandlingType = "EXCEPTION"

    def create(self):
        self.newInput("Integer", "Sides", "sides", value = 3, minValue = 3)
        self.newInput("Float", "Radius", "radius", value = 1)

        self.newOutput("Mesh", "Mesh", "mesh")

    def execute(self, sides, radius):
        vertexList = []
        edgeList = []
        polygonList = []
        
        for side in range(sides):
            posX = ( math.sin( side / sides * 2 * math.pi ) * radius )
            posY = ( math.cos( side / sides * 2 * math.pi ) * radius )
            posZ = 0 # 0 since mesh is 2D (1 polygon)
            vertexList.append((posX, posY, posZ))
            if (side < sides-1):
                edgeList.append((side, side+1))
            else:
                edgeList.append((side, 0)) # last vertex (connects with the first)
            polygonList.append(side)

        vertexLocations = Vector3DList.fromValues(vertexList)
        edgeIndices = EdgeIndicesList.fromValues(edgeList)
        formattedPolygonList = [tuple(polygonList)] # the list needs to be a "list" (type) containing tuples
        polygonIndices = PolygonIndicesList.fromValues(formattedPolygonList)
        mesh = Mesh(vertexLocations, edgeIndices, polygonIndices)

        return mesh.copy()

