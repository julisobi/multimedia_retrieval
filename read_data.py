import trimesh
import os
import glob
from tqdm import tqdm
import matplotlib.pyplot as plt

FILE = 'm107.off'
FILE2 = 'car_wheel_cap.ply'
DIR = 'LabeledDB_new'
trimesh.util.attach_to_log()


def view_3d(file):
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


output = []
i = 0

# The following three variables are for the histograms
vertice_nums = []
category_nums = []
faces_nums = []

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

            # Append the necessary info to variables for histograms
            vertice_nums.append(int(num_vert))
            category_nums.append(str(dir))
            faces_nums.append(int(num_faces))

        mesh = trimesh.load(filename, force='mesh')
        new_dict = {"shape_class": str(dir), "num_verticles": int(num_vert), "num_faces": int(num_faces),
                    "faces_type": str(type_of_faces), "axis_bound_box": mesh.bounding_box, "bound_box": mesh.bounding_box_oriented }
        output.append(new_dict)
        i += 1
print(f"Number of 3D objects in dataset: {i}")
print(output)

# Distribution of amount of vertices before preprocessing
plt.hist(vertice_nums, rwidth=0.95, bins=15)
plt.title('Distribution of amount of vertices')
plt.ylabel('frequency')
plt.xlabel('# of vertices')
plt.show()

# Distribution of different categories before preprocessing
plt.hist(category_nums, rwidth=0.95, bins=19)
plt.xticks(rotation=90)
plt.title('Distribution of categories')
plt.ylabel('frequency')
plt.xlabel('category')
plt.show()

# Distribution of amount of faces before preprocessing
plt.hist(faces_nums, rwidth=0.95, bins=15)
plt.title('Distribution of amount of faces')
plt.ylabel('frequency')
plt.xlabel('# of faces')
plt.show()


# print(output)
# view_3d(FILE)
