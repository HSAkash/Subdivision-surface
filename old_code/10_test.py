
import numpy as np
import trimesh

# Create a new plot
object_mesh = trimesh.load_mesh('data-li/tower.ply')
# get points and face index
vertices = object_mesh.vertices
edges = object_mesh.edges
faces = object_mesh.faces
# Create a new plot
# mesh = trimesh.Trimesh(vertices=vertices, vertex_indices=vertex_indices, process=False)
mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)

# change the color of the mesh
mesh.visual.face_colors = [255, 0, 0, 100]

# plot the mesh, returning a matplotlib axis
ax = trimesh.Scene(mesh).show()



