import trimesh
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
    


if __name__ == '__main__':
    mesh_path = input("Enter path to mesh (.ply): ")
    iterations = int(input("Enter number of iterations: "))
    save_png = input("Save png? (y/n): ")
    if save_png == 'y':
        save_png = True
        save_png_path = input("Enter path to save png (.png/.jpg/.jpeg): ")
    else:
        save_png = False
    print(f"Color inputs")
    R = int(input("Red 0-255 : "))
    G = int(input("Green 0-255 : "))
    B = int(input("Blue 0-255 : "))
    Opacity = int(input("Opacity 0-255 : "))
    # object_mesh = trimesh.load_mesh('data-li/tower.ply')
    object_mesh = trimesh.load_mesh(mesh_path)
    input_points = object_mesh.vertices
    if 'vertex_indices' in object_mesh.metadata['_ply_raw']['face']['data'].keys():
        input_faces = object_mesh.metadata['_ply_raw']['face']['data']['vertex_indices']
    else:
        input_faces = object_mesh.metadata['_ply_raw']['face']['data']['vertex_index']

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