import trimesh
import os
import glob

FILE = 'm107.off'
FILE2 = 'car_wheel_cap.ply'
DIR = 'LabeledDB_new'
trimesh.util.attach_to_log()


def view_3d(file):
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


output = []
i = 0
for dir in os.listdir(DIR):
    for filename in glob.iglob(f'{DIR}/{dir}/*.off'):
        with open(filename) as f:
            second_line = f.readlines()[1]
            num_faces = second_line.split()[1]
            num_vert = second_line.split()[0]
        new_dict = {"shape_class": str(dir), "num_verticles": num_vert, "num_faces": num_faces}
        output.append(new_dict)
        i += 1
print(f"Number of 3D objects in dataset: {i}")


# print(output)
# view_3d(FILE)
