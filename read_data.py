import trimesh
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
import math

FILE = 'm107.off'
FILE2 = 'lobster.ply'
DIR = 'LabeledDB_new'
trimesh.util.attach_to_log()


def view_3d(file):
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


def x_y_z(file):
    x, y, z = [], [], []
    with open(file) as f:
        for line in f.readlines()[2:]:
            if line[:2] not in ['3 ', '4 ']:
                x.append(line.split()[0])
                y.append(line.split()[1])
                z.append(line.split()[2])
    return x, y, z


def pca(file):
    x_coords, y_coords, z_coords = x_y_z(file)
    n_points = len(x_coords)

    A = np.zeros((3, n_points))
    A[0] = x_coords
    A[1] = y_coords
    A[2] = z_coords

    A_cov = np.cov(A)  # 3x3 matrix
    eigenvalues, eigenvectors = np.linalg.eig(A_cov)

    print("==> eigenvalues for (x, y, z)")
    print(eigenvalues)
    print("\n==> eigenvectors")
    print(eigenvectors)


def normalization_tool(file):
    mesh = trimesh.load(file, force='mesh')

    # Normalization of position
    translate_matrix = [[1, 0, 0, -mesh.center_mass[0]],
                        [0, 1, 0, -mesh.center_mass[1]],
                        [0, 0, 1, -mesh.center_mass[2]],
                        [0, 0, 0, 1]]
    mesh.apply_transform(translate_matrix)

    # Alignment
    n_points = len(mesh.vertices)
    A = np.zeros((3, n_points))
    A[0] = mesh.vertices.transpose()[0]
    A[1] = mesh.vertices.transpose()[1]
    A[2] = mesh.vertices.transpose()[2]
    A_cov = np.cov(A)
    eigenvalues, eigenvectors = np.linalg.eig(A_cov)
    e1_e2 = np.cross(eigenvectors[0], eigenvectors[1])
    E = np.zeros((3, 3))
    E[0] = eigenvectors[0]
    E[1] = eigenvectors[1]
    E[2] = e1_e2
    updated = np.dot(A.transpose(), E)
    mesh.vertices = updated

    # Normalization scale
    bound_box = mesh.bounding_box
    smallest = max(bound_box.extents)
    scale = 1 / smallest

    scale_matrix = [[scale, 0, 0, 0],
                    [0, scale, 0, 0],
                    [0, 0, scale, 0],
                    [0, 0, 0, 1]]

    mesh.apply_transform(scale_matrix)
    return mesh, E


def save_ouput(fold):
    output = []
    i = 0
    vertice_nums = []
    category_nums = []
    faces_nums = []
    norm_dist = []
    long_boundbox = []
    amount_quads = 0

    for dir in tqdm(os.listdir(fold)):
        for filename in glob.iglob(f'{fold}/{dir}/*.off'):
            mesh, Eigen = normalization_tool(filename)
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
                    amount_quads = amount_quads + 1
                elif triangles:
                    type_of_faces = 'triangles'
                elif quads:
                    type_of_faces = 'quads'
                    amount_quads = amount_quads + 1
                num_faces = second_line.split()[1]
                num_vert = second_line.split()[0]

                #mesh = trimesh.load(filename, force='mesh')
                p1 = np.array([mesh.center_mass[0], mesh.center_mass[1], mesh.center_mass[2]])
                p2 = np.array([0, 0, 0])
                dist = distance_two_point(p1, p2)


                # Append the necessary info to variables for histograms
                vertice_nums.append(int(num_vert))
                category_nums.append(str(dir))
                faces_nums.append(int(num_faces))
                norm_dist.append(dist)
                long_boundbox.append(round(float(max(mesh.bounding_box.extents)), 5))

            # Comment line under this one and uncomment the on under that if you don't want to wait for hours.
            diam = diameter(mesh)
            #diam = 0

            #if str(type_of_faces) == "triangles":
            new_dict = {"shape_class": str(dir),
                        "num_verticles": int(num_vert),
                        "num_faces": int(num_faces),
                        "faces_type": str(type_of_faces),
                        "axis_bound_box": mesh.bounding_box.extents,
                        "bound_box": mesh.bounding_box_oriented.extents,
                        "path": filename,
                        "watertight": mesh.is_watertight,
                        "area": mesh.area,
                        "volume": mesh.volume,
                        "compactness": mesh.area ** 3 / mesh.bounding_sphere.volume,
                        "diameter": diameter,
                        "eccentricity": (Eigen[0] / Eigen[2]),
                        "bound_box_volume": mesh.bounding_box_oriented.volume}
            output.append(new_dict)
            i += 1

    print(f"Number of 3D objects in dataset: {i}")
    return output


def diameter(mesh):
    diam = 0
    print(mesh.vertices[0])
    for vertex in mesh.vertices:
        a = np.array([vertex[0], vertex[1], vertex[2]])
        for vertex2 in mesh.vertices:
            b = np.array([vertex2[0], vertex2[1], vertex2[2]])
            if distance_two_point(a, b) > diam:
                diam = abs(np.linalg.norm(a-b))
    return diam

def distance_two_point(p1, p2):
    #p1 = np.array([x1_coords, y1_coords, z1_coords])
    #p2 = np.array([x2_coords, y2_coords, z2_coords])
    squared_dist = np.sum((p1 - p2) ** 2, axis=0)
    return np.sqrt(squared_dist)


def norm_plots(dist_list, bound_list):
    # Distribution of amount of vertices before preprocessing
    plt.hist(dist_list, rwidth=0.95, bins=15)
    plt.title('Distribution of distances between barycenter of meshes and the world origin')
    plt.ylabel('frequency')
    plt.xlabel('distance to origin')
    plt.show()

    # Distribution of amount of vertices before preprocessing
    plt.hist(bound_list, rwidth=0.95, bins=15)
    plt.title('Distribution of the longest size of the axis-aligned bounding box of the mesh ')
    plt.ylabel('frequency')
    plt.xlabel('size of longest side of the bounding box')
    plt.show()


def save_excel(folder):
    out = save_ouput(folder)
    df = pd.DataFrame.from_dict(out)
    df.to_excel('filter.xlsx')


def before_and_after_scale_images():
    mesh2 = trimesh.load('unit_cube.off', force='mesh')
    mesh = trimesh.load('m107.off', force='mesh')

    print("center before", mesh.center_mass)

    translate_matrix = [[1, 0, 0, -mesh.center_mass[0]],
                        [0, 1, 0, -mesh.center_mass[1]],
                        [0, 0, 1, -mesh.center_mass[2]],
                        [0, 0, 0, 1]]
    mesh.apply_transform(translate_matrix)
    (mesh + mesh2).show()

    print("center after", mesh.center_mass)

    bound_box = mesh.bounding_box
    biggest = max(bound_box.extents)
    scale = 1 / biggest

    scale_matrix = [[scale, 0, 0, 0],
                    [0, scale, 0, 0],
                    [0, 0, scale, 0],
                    [0, 0, 0,     1]]

    mesh.apply_transform(scale_matrix)
    print(mesh.bounding_box.extents)
    (mesh + mesh2).show()

# # uncomment the line below to save the excel file
save_excel(DIR)

#mesh = trimesh.load(FILE, force='mesh')
#diam = diameter(mesh)

#normalization_tool(FILE)