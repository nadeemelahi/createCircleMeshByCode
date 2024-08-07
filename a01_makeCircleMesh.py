#
# author: Nadeem Elahi
# nadeem.elahi@gmail.com
# nad@3deem.com
# license: gpl v3
# 

import bpy
import numpy
from math import sin
from math import cos 
from math import radians



def reset() :
	#https://blenderartists.org/t/deleting-all-from-scene/1296469
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False)



def fullReset() :
	#https://blenderartists.org/t/deleting-all-from-scene/1296469
	bpy.ops.object.select_all(action='SELECT')
	bpy.ops.object.delete(use_global=False)

	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()
	bpy.ops.outliner.orphans_purge()



def printVerts ( vertices ) :
    idx = 0
    lim = len ( vertices ) 

    while idx < lim :

        print ( idx , ":" , vertices[idx]  )

        idx += 1



#
def printVerts ( vertices ) :
	idx = 0
	lim = len ( vertices ) 

	while idx < lim :

		print ( idx , vertices [ idx ]  )

		idx += 1



# copy verts [cnt] number of verts from src to dst 
#   with supplied start idx for each
def copyArray ( 
		vertsSrc , srcStartIdx ,
		vertsDst , dstStartIdx , 
		cnt 
		) :

	idx = 0
	while idx < cnt :

		vertsDst[dstStartIdx + idx][0] = vertsSrc[idx][0]
		vertsDst[dstStartIdx + idx][1] = vertsSrc[idx][1]
		vertsDst[dstStartIdx + idx][2] = vertsSrc[idx][2]

		idx += 1


# set the same z value on a [cnt] number of verts
# useful for extruding a given geometry
def setVertZ ( verts , startIdx, cnt , zloc ) :

	idx = 0
	while idx < cnt :

		verts[idx + startIdx][2] = zloc

		idx += 1







#fullReset()
reset()


# coverts from radial to rectangular coordinate systems
def radial2rectX ( angle ) :
    return cos ( radians ( angle ) )

def radial2rectY ( angle ) :
    return sin ( radians ( angle ) )


# algorithm/equation index*(360/division)
def makeCirclePrimitive ( divisions , verts , faces ) :

    # center vert
    verts[  0 ] = (  0.0 ,  0.0 , 0.0 ) 

    # verts loop
    angle = 0
    angleStep = 360 / divisions

    rectx = 0
    recty = 0

    idx = 1
    limVertsLoop = divisions + 1

    while idx < limVertsLoop :

        rectx = radial2rectX ( angle )
        recty = radial2rectY ( angle )
        verts [ idx ] = ( rectx , recty , 0.0 ) 

        angle = idx * angleStep 
        idx += 1
        

    # faces loop
    idx = 0
    centerIndex = 0
    lastIndex = divisions
    limFacesLoop = divisions - 1 

    while idx < limFacesLoop :

        faces [ idx ] = ( 0 , idx + 1 , idx + 2 )

        idx += 1

    faces [ idx ] = ( 0 , lastIndex , 1 ) 




# set desired resolution(divisions count) 
divisions = 100

vertsBufferSize = divisions + 1
facesBufferSize = divisions 

#          buffer size 100 , 3 dimensional each
verts = numpy.zeros( ( vertsBufferSize , 3 ) , dtype=float )
# 100 -> 3D arrays

faces = numpy.zeros( ( facesBufferSize , 3 ) , dtype=int )


makeCirclePrimitive ( divisions , verts , faces )
print( "verts" ) 
printVerts ( verts )
print( "faces" )
printVerts ( faces )

name = "name"

# verts to mesh
mesh = bpy.data.meshes.new ( name )
mesh.from_pydata ( verts , [] , faces )

# mesh to obj
obj = bpy.data.objects.new ( name , mesh )

# add ojb to scene
bpy.context.scene.collection.objects.link ( obj ) 
