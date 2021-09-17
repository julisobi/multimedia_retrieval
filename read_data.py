import trimesh

FILE = 'm107.off'
FILE2 = 'car_wheel_cap.ply'
trimesh.util.attach_to_log()


def view_3d(file):
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


view_3d(FILE)
