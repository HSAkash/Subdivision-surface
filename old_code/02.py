from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np
import sys
import trimesh

import matplotlib
matplotlib.use('Qt5Agg')



def plot_mesh(vertices, faces):
    # Create a new plot
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)

    # change the color of the mesh

    # plot the mesh, returning a matplotlib axis
    mesh.visual.face_colors = [0, 255, 0,100]
    # # color the mesh
    mesh.visual.vertex_colors = [255, 255, 0, 150]
    # mesh.visual.face_colors = [0, 255, 0, 255]
    # mesh.visual.face_colors = [0, 255, 0]
    # mesh.visual.face_colors = [0, 255, 0, 255]


    ax = trimesh.Scene(mesh)
    

    ax.show()





    


if __name__ == "__main__":
    # Create a new plot
    object_mesh = trimesh.load_mesh('data-ply/duck_refine.ply')
    # get points and face index
    vertices = object_mesh.vertices
    # print(f"vertices: {vertices}")
    edges = object_mesh.edges
    faces = object_mesh.faces
    plot_mesh(vertices, faces)
    # print(vertices.shape, edges.shape, faces.shape)
    # print(object_mesh.metadata)

    """.obj"""
    # print(object_mesh.vertex_faces)


    # """if .ply"""
    # print(object_mesh.metadata['_ply_raw']['face']['data']['vertex_indices'])

    # print(object_mesh.metadata)
    # print(object_mesh.metadata['_ply_raw']['face']['data']['vertex_indices'])
    # print(object_mesh.metadata['_ply_raw']['face']['data']['vertex_index'])