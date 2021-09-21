import trimesh
import os
import glob
from tqdm import tqdm

FILE = 'm107.off'
FILE2 = 'car_wheel_cap.ply'
DIR = 'LabeledDB_new'
trimesh.util.attach_to_log()


def view_3d(file):
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


output = []
i = 0
for dir in tqdm(os.listdir(DIR)):
    for filename in glob.iglob(f'{DIR}/{dir}/*.off'):
        triangles = False
        quads = False
        type_of_faces = ''
        with open(filename) as f:
            num_line = 1
            for line in f.readlines():
                if num_line == 2:
                    second_line = line
                if line[0] == '3':
                    triangles = True
                elif line[0] == '4':
                    quads = True
                num_line += 1
            if triangles and quads:
                type_of_faces = 'mix'
            elif triangles:
                type_of_faces = 'triangles'
            elif quads:
                type_of_faces = 'quads'
            num_faces = second_line.split()[1]
            num_vert = second_line.split()[0]
        new_dict = {"shape_class": str(dir), "num_verticles": num_vert, "num_faces": num_faces,
                    "faces_type": str(type_of_faces)}
        output.append(new_dict)
        i += 1
print(f"Number of 3D objects in dataset: {i}")
print(output)

# print(output)
# view_3d(FILE)
