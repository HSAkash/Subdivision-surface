import trimesh

mesh = trimesh.load_mesh('data-li/tower002.obj')

# obj to ply
mesh.export('data-li/tower002.ply', file_type='ply')

