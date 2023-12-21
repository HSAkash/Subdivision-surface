import re
import os
import numpy as np
import pyvista as pv
from tqdm import tqdm
from glob import glob
from cmc import cmc_subdiv
import matplotlib.pyplot as plt

iterations_dir = "iterations"


def read_obj(filename):
    vertices = []
    faces = []

    with open(filename, 'r') as f:
        for line in f:
            parts = re.split(r'\s+', line.strip())

            if parts[0] == 'v':
                vertices.append(parts[1:4])
            elif parts[0] == 'f':
                face = [int(p.split('/')[0]) for p in parts[1:]]
                faces.append(face)

    return list(np.array(vertices, dtype=np.float32)), list(np.array(faces, dtype=int)-1)

def write_obj(filename, vertices, faces):
    with open(filename, 'w') as f:
        for v in list(np.array(vertices, dtype=np.float32)):
            f.write(f"v {' '.join(map(str, v))}\n")
        for face in list(np.array(faces)+1):
            f.write(f"f {' '.join(map(str, face))}\n")


def show_obj(
    obj_path='',
    initial_obj_path=None,
    cmap='coolwarm',
    cmap_axis = 1,
    show_edges=True,
    edge_color='blue',
    edge_width=1,
    show_points=True,
    point_color='red',
    point_size=2,
    initial_mesh_edge_color='black',
    initial_mesh_edge_width=1,
    show_initial_points=True,
    initial_mesh_point_color='black',
    initial_mesh_point_size=2,
    show_edges_only=True,
    ):
    # Create a Plotter object
    plotter = pv.Plotter()

    # Load the mesh
    mesh = pv.read(obj_path)

    # Add the full mesh to the plotter
    if not show_edges_only:
        scalars = mesh.points[:, cmap_axis]  # Use the z-coordinates
        # Add the scalar values to the mesh
        mesh.point_data["scalars"] = scalars
        # Add the full mesh to the plotter with the colormap
        plotter.add_mesh(mesh, cmap=cmap, scalars="scalars")



    # Extract the edges and add them to the plotter
    if show_edges and edge_color:
        edges = mesh.extract_all_edges()
        plotter.add_mesh(edges, color=edge_color, line_width=edge_width)

    # Create a point cloud from the points of the mesh
    if show_points and point_color:
        points = pv.PolyData(mesh.points)
        # Add the points to the plotter with a specific size and color
        plotter.add_points(points, color=point_color, point_size=point_size)


    if initial_obj_path:
        initial_mesh = pv.read(initial_obj_path)
        initial_edges = initial_mesh.extract_all_edges()
        plotter.add_mesh(initial_edges, color=initial_mesh_edge_color,
                        line_width=initial_mesh_edge_width)
        if show_initial_points:
            initial_points = pv.PolyData(initial_mesh.points)
            plotter.add_points(initial_points, color=initial_mesh_point_color,
                            point_size=initial_mesh_point_size)


    plotter.show()



def Input_func():
    obj_path='',
    initial_obj_path=None,
    cmap='coolwarm',
    cmap_axis = 1,
    show_edges=True,
    edge_color='blue',
    edge_width=1,
    show_points=True,
    point_color='red',
    point_size=2,
    initial_mesh_edge_color='black',
    initial_mesh_edge_width=1,
    show_initial_points=True,
    initial_mesh_point_color='black',
    initial_mesh_point_size=2
    show_edges_only=True
    loop_cmap=False

    obj_path = input("Enter the path to the obj file: ") # Mesh object path
    iterations = int(input("Enter the number of iterations: ")) # Number of iterations
    show_edges = input("Show edges: y/n: ") # Show edges
    show_edges = True if show_edges.lower()=='y' else False
    if show_edges:
        edge_color = input("Enter edge color: ")
        edge_width = int(input("Enter edge width: "))
    show_points = input("Show points: y/n: ") # Show points
    show_points = True if show_points.lower()=='y' else False
    if show_points:
        point_color = input("Enter point color: ")
        point_size = int(input("Enter point size: "))

    initial_mesh = input("Show initial mesh edge: y/n: ")
    initial_mesh = initial_mesh.lower()
    initial_obj_path = None
    if initial_mesh=='y':
        initial_obj_path = obj_path
        initial_mesh_edge_color = input("Enter initial mesh edge color: ")
        initial_mesh_edge_width = int(input("Enter initial mesh edge width: "))
        show_initial_points = input("Show initial mesh points: y/n: ")
        show_initial_points = True if show_initial_points.lower()=='y' else False
        if show_initial_points:
            initial_mesh_point_color = input("Enter initial mesh point color: ")
            initial_mesh_point_size = int(input("Enter initial mesh point size: "))

    show_edges_only = input("Show edges only: y/n: ")
    show_edges_only = True if show_edges_only.lower()=='y' else False
    if not show_edges_only:
        loop_cmap = input("Loop color map: y/n: ")
        loop_cmap = True if loop_cmap.lower()=='y' else False
        if not loop_cmap:
            cmap = input("Enter color map: ")
        cmap_axis = input("Enter color map axis (x/y/z) : ")
        cmap_axis = 0 if cmap_axis=='x' else 1 if cmap_axis=='y' else 2

    
    return obj_path, iterations, cmap, cmap_axis, show_edges, edge_color, edge_width, show_points, point_color, point_size, initial_obj_path, initial_mesh_edge_color, initial_mesh_edge_width, show_initial_points, initial_mesh_point_color, initial_mesh_point_size, show_edges_only, loop_cmap


def main():
    obj_path, iterations, cmap, cmap_axis, show_edges, edge_color, edge_width, show_points, point_color, point_size, initial_obj_path, initial_mesh_edge_color, initial_mesh_edge_width, show_initial_points, initial_mesh_point_color, initial_mesh_point_size, show_edges_only, loop_cmap = Input_func()
    

    obj_file_name = obj_path.replace(".obj", "").split("/")[-1] # Name of the obj file
    os.makedirs(f"{iterations_dir}/{obj_file_name}", exist_ok=True) # Create a directory to store the iterations

    iterated_obj_list = glob(f"{iterations_dir}/{obj_file_name}/*.obj")
    initial_iterations = 0
    
    if len(iterated_obj_list) > 0:
        for iter_obj in iterated_obj_list:
            iter_index = int(iter_obj.split("/")[-1].replace(".obj", ""))
            initial_iterations = max(initial_iterations, iter_index)

    print(f"Starting from iteration {initial_iterations+1}")
    
    for i in tqdm(range(initial_iterations+1,iterations+1)):
        save_obj_path = os.path.join(iterations_dir, obj_file_name, f"{i:0>2}.obj")
        vertices, faces = read_obj(obj_path)
        output_points, output_faces = cmc_subdiv(vertices, faces)
        write_obj(save_obj_path, output_points, output_faces)
        # release resources
        del output_points
        del output_faces
        del vertices
        del faces
        obj_path = save_obj_path


    show_obj_path = os.path.join(iterations_dir, obj_file_name, f"{iterations:0>2}.obj")

    if not os.path.exists(show_obj_path) or iterations==0:
        show_obj_path = obj_path
    print(f"Saved the final iteration to {show_obj_path}")
    # show_obj(show_obj_path) # Show the final iteration
    if loop_cmap:
        for cmap in plt.colormaps():
            show_obj(
                show_obj_path,
                initial_obj_path=initial_obj_path,
                cmap=cmap,
                cmap_axis = cmap_axis,
                show_edges=show_edges,
                edge_color=edge_color,
                edge_width=edge_width,
                show_points=show_points,
                point_color=point_color,
                point_size=point_size,
                initial_mesh_edge_color=initial_mesh_edge_color,
                initial_mesh_edge_width=initial_mesh_edge_width,
                show_initial_points=show_initial_points,
                initial_mesh_point_color=initial_mesh_point_color,
                initial_mesh_point_size=initial_mesh_point_size,
                show_edges_only=show_edges_only
            )
    else:
        show_obj(
            show_obj_path,
            initial_obj_path=initial_obj_path,
            cmap=cmap,
            cmap_axis = cmap_axis,
            show_edges=show_edges,
            edge_color=edge_color,
            edge_width=edge_width,
            show_points=show_points,
            point_color=point_color,
            point_size=point_size,
            initial_mesh_edge_color=initial_mesh_edge_color,
            initial_mesh_edge_width=initial_mesh_edge_width,
            show_initial_points=show_initial_points,
            initial_mesh_point_color=initial_mesh_point_color,
            initial_mesh_point_size=initial_mesh_point_size,
            show_edges_only=show_edges_only
        )



if __name__ == "__main__":
    main()
