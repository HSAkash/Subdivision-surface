import trimesh
import argparse
from cmc import cmc_subdiv
from pyglet import gl


def save_mesh_png(scene, path='output.png'):
        window_conf = gl.Config(double_buffer=True, depth_size=6)
        # run the actual render call                                                             
        png = scene.save_image(resolution=[1920, 1080], visible=True, window_conf=window_conf)
        
        # byte objects save the image
        with open(path, 'wb') as f:
            f.write(png)



def plot_mesh(vertices, faces, colors):
    # Create a new plot
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces, process=False)
    # color the mesh
    # mesh.visual.face_colors = [R, G, B, Opacity]
    mesh.visual.face_colors = colors

    scene = trimesh.Scene(mesh)
    scene.show()
    return scene

def get_arguments():
    parser = argparse.ArgumentParser(description='CMC Subdivision')
    parser.add_argument('--mesh', type=str, help='path to mesh file')
    parser.add_argument('--iterations', type=int, default=1, help='number of iterations')
    parser.add_argument('--yes-save', action='store_true', help='save figure as image')
    parser.add_argument('--path', type=str, default='output.png', help='image save path')
    parser.add_argument('--R', type=int, default=0, help='Red 0-255')
    parser.add_argument('--G', type=int, default=0, help='Green 0-255')
    parser.add_argument('--B', type=int, default=0, help='Blue 0-255')
    parser.add_argument('--Opacity', type=int, default=255, help='Opacity 0-255')
    return parser.parse_args()
    


if __name__ == '__main__':

    args = get_arguments()
    mesh_path = args.mesh
    iterations = args.iterations
    save_png = args.yes_save
    save_png_path = args.path
    R = args.R
    G = args.G
    B = args.B
    Opacity = args.Opacity

    
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

    for i in range(iterations):
        output_points, output_faces = cmc_subdiv(output_points, output_faces)


    # plot mesh points
    scene = plot_mesh(vertices=output_points, faces=output_faces, colors=[R, G, B, Opacity])

    if save_png:
        extention = save_png_path.split('.')[-1]
        if extention not in ['png', 'jpg', 'jpeg','.PNG']:
            save_png_path += '.png'
        save_mesh_png(scene, save_png_path)
        print(f"Saved png to {save_png_path}")