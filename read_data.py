import trimesh
import os
import glob
import pandas as pd
from tqdm import tqdm

FILE = 'm107.off'
FILE2 = 'car_wheel_cap.ply'
DIR = 'LabeledDB_new'
trimesh.util.attach_to_log()


def view_3d(file):
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


def save_ouput(fold):
    output = []
    i = 0
    vertice_nums = []
    category_nums = []
    faces_nums = []

    for dir in tqdm(os.listdir(fold)):
        for filename in glob.iglob(f'{fold}/{dir}/*.off'):
            triangles, quads = False, False
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

            # Normalization of position
            translate_matrix = [[1, 0, 0, -mesh.center_mass[0]],
                                [0, 1, 0, -mesh.center_mass[1]],
                                [0, 0, 1, -mesh.center_mass[2]],
                                [0, 0, 0, 1]]
            mesh.apply_transform(translate_matrix)

            # Normalization scale
            bound_box = mesh.bounding_box
            smallest = max(bound_box.extents)
            scale = 1 / smallest

            scale_matrix = [[scale, 0, 0, 0],
                            [0, scale, 0, 0],
                            [0, 0, scale, 0],
                            [0, 0, 0, scale]]

            mesh.apply_transform(scale_matrix)

            new_dict = {"shape_class": str(dir), "num_verticles": int(num_vert), "num_faces": int(num_faces),
                        "faces_type": str(type_of_faces), "axis_bound_box": bound_box,
                        "bound_box": mesh.bounding_box_oriented, "path": filename}
            output.append(new_dict)
            i += 1
    print(f"Number of 3D objects in dataset: {i}")
    return output


def save_excel(folder):
    out = save_ouput(folder)
    df = pd.DataFrame.from_dict(out)
    df.to_excel('filter.xlsx')


# # uncomment the line below to save the excel file
save_excel(DIR)
