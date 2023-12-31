import trimesh
from cmc import cmc_subdiv
from vedo import trimesh2vedo, show, Line, Plotter, Points, Lines
import matplotlib.pyplot as plt
from tqdm import tqdm


def plot_mesh(vertices,
              faces,edge_plot_bool,
              cmap="magma",
              edge_color='black',
              edge_width=4,
              point_color='green',
              point_size=5,
              only_edge=False):
    meshe = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    vmeshes = trimesh2vedo(meshe)
    # Define some dummy point scalar
    scals = vmeshes.points()[:,0]
    # vmeshes.cmap("jet", scals)
    vmeshes.cmap(cmap, scals)

    # Create a Plotter object
    plotter = Plotter()

    if not only_edge:
        # Add the mesh to the plotter
        plotter.add(vmeshes)

    # Add edges to the plot
    if edge_plot_bool:
        print(f"________________________Edge Ploting Started___________________________")
        edges = meshe.edges
        lines = Lines(meshe.vertices[edges], c=edge_color, lw=edge_width)
        plotter.add(lines)
        print(f"________________________Edge Ploting End___________________________")
        # Add vertices to the plot
        vertices = Points(meshe.vertices, r=point_size, c=point_color)
        plotter.add(vertices)

    # Show the plot with no axes or background grid
    plotter.show(axes=None)


def plot_mesh_with_initial(
        vertices,
        faces,
        initial_mesh,
        edge_plot_bool,
        cmap="magma",
        edge_color='black',
        edge_width=4,
        point_color='green',
        point_size=5,
        initial_edge_color='black',
        initial_edge_width=4,
        initial_point_color='green',
        initial_point_size=5,
        only_edge=False):
    meshe = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    vmeshes = trimesh2vedo(meshe)
    # Define some dummy point scalar
    scals = vmeshes.points()[:,0]
    # vmeshes.cmap("jet", scals)
    vmeshes.cmap(cmap, scals)

    # Create a Plotter object
    plotter = Plotter()

    if not only_edge:
        # Add the mesh to the plotter
        plotter.add(vmeshes)

    # Add edges to the plot
    if edge_plot_bool:
        print(f"________________________Edge Ploting Started___________________________")
        edges = meshe.edges
        lines = Lines(meshe.vertices[edges], c=edge_color, lw=edge_width)
        plotter.add(lines)
        

        # Add vertices to the plot
        vertices = Points(meshe.vertices, r=point_size, c=point_color)
        plotter.add(vertices)

        initial_edge = initial_mesh.edges
        lines = Lines(initial_mesh.vertices[initial_edge], c=initial_edge_color, lw=initial_edge_width)
        plotter.add(lines)

        initial_vertices = Points(initial_mesh.vertices, r=initial_point_size, c=initial_point_color)
        plotter.add(initial_vertices)
        print(f"________________________Edge Ploting End___________________________")

    # Show the plot with no axes or background grid
    plotter.show(axes=None)






if __name__ == '__main__':

    mesh_path = input("Enter mesh path: ")
    iterations = int(input("Enter number of iterations: "))
    # cmap = input("Enter color map: ")
    edge_color = input("Enter edge color: ")
    edge_width = int(input("Enter edge width: "))
    point_color = input("Enter point color: ")
    point_size = int(input("Enter point size: "))
    edge_plot_bool = input("Show edge plot: y/n: ")
    only_edge = input("Only edge plot: y/n: ")
    initial_mesh = input("Show initial mesh edge: y/n: ")
    initial_mesh = initial_mesh.lower()

    
    edge_plot_bool = True if edge_plot_bool.lower()=='y' else False
    only_edge = True if only_edge.lower()=='y' else False

    if initial_mesh=='y':
        initial_mesh_edge_color = input("Enter initial mesh edge color: ")
        initial_mesh_edge_width = int(input("Enter initial mesh edge width: "))
        initial_mesh_point_color = input("Enter initial mesh point color: ")
        initial_mesh_point_size = int(input("Enter initial mesh point size: "))


    
    try:
        object_mesh = trimesh.load_mesh(mesh_path)
        input_points = object_mesh.vertices
        if 'vertex_indices' in object_mesh.metadata['_ply_raw']['face']['data'].keys():
            input_faces = object_mesh.metadata['_ply_raw']['face']['data']['vertex_indices']
        else:
            input_faces = object_mesh.metadata['_ply_raw']['face']['data']['vertex_index']
    except:
        print(f"""_________________________Error___________________________""")
        print("Error loading mesh file")
        exit(1)

    



    output_points, output_faces = input_points, input_faces
    print(f"________________________Iteration Started___________________________")
    for i in tqdm(range(iterations)):
        output_points, output_faces = cmc_subdiv(output_points, output_faces)
    print(f"________________________Iteration Completed___________________________")

    print(f"""
Total number of new vertices: {len(output_points)}
Total number of new faces: {len(output_faces)}
    """)
    # plot_mesh(output_points, output_faces, cmap=cmap, edge_color=edge_color, edge_width=edge_width, point_color=point_color, point_size=point_size)
    if initial_mesh == 'y':
        for cmap in plt.colormaps():
            plot_mesh_with_initial(
                output_points,
                output_faces,
                object_mesh,
                edge_plot_bool,
                cmap=cmap,
                edge_color=edge_color,
                edge_width=edge_width,
                point_color=point_color,
                point_size=point_size,
                initial_edge_color=initial_mesh_edge_color,
                initial_edge_width=initial_mesh_edge_width,
                initial_point_color=initial_mesh_point_color,
                initial_point_size=initial_mesh_point_size,
                only_edge=only_edge
            )
            
            if only_edge:
                break
    else:
        for cmap in plt.colormaps():
            plot_mesh(
                output_points,
                output_faces,
                edge_plot_bool,
                cmap=cmap,
                edge_color=edge_color,
                edge_width=edge_width,
                point_color=point_color,
                point_size=point_size,
                only_edge=only_edge
            )
            if only_edge:
                break
