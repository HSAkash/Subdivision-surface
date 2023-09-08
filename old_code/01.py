from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import sys
import trimesh

import matplotlib
matplotlib.use('Qt5Agg')

# Create a new plot
object_mesh = trimesh.load_mesh('data-li/tower.ply')

# change the color of the mesh
object_mesh.visual.face_colors = [255, 0, 0, 100]
# get points and face index
points = object_mesh.vertices
faces = object_mesh.faces

print(points.shape, faces.shape)


# plot the mesh, returning a matplotlib axis
ax = trimesh.Scene(object_mesh).show()





