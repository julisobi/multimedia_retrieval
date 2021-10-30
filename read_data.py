import trimesh
import os
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.spatial import ConvexHull
from scipy.spatial.distance import cdist
import feature_extraction as fe

FILE = 'm107.off'
FILE2 = 'Bust_305.off'
DIR = 'LabeledDB_new'
VOLUME = 'V1_141_chair.off'
trimesh.util.attach_to_log()


def view_3d(file):
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


def position(mesh):
    translate_matrix = [[1, 0, 0, -mesh.center_mass[0]],
                        [0, 1, 0, -mesh.center_mass[1]],
                        [0, 0, 1, -mesh.center_mass[2]],
                        [0, 0, 0, 1]]
    mesh.apply_transform(translate_matrix)
    return mesh


def alignment(mesh):
    # numpy.linalg.eigvals?
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
    updated = np.zeros((n_points, 3))
    A = A.transpose()
    for i in range(n_points):
        updated[i] = np.dot(A[i], eigenvectors)
    mesh.vertices = updated
    return mesh, E, eigenvalues


def orientation(mesh):
    fx, fy, fz = [], [], []
    for i in range(len(mesh.triangles)):
        Cx = sum(mesh.triangles[i][:, 0]) / 3
        sign_Cx = np.sign(Cx)
        sq_Cx = np.square(Cx)
        fx.append(sign_Cx * sq_Cx)

        Cy = sum(mesh.triangles[i][:, 1]) / 3
        sign_Cy = np.sign(Cy)
        sq_Cy = np.square(Cy)
        fy.append(sign_Cy * sq_Cy)

        Cz = sum(mesh.triangles[i][:, 2]) / 3
        sign_Cz = np.sign(Cz)
        sq_Cz = np.square(Cz)
        fz.append(sign_Cz * sq_Cz)

    fx_value = sum(fx)
    fy_value = sum(fy)
    fz_value = sum(fz)
    mesh.vertices[:, 0] *= np.sign(fx_value)
    mesh.vertices[:, 1] *= np.sign(fy_value)
    mesh.vertices[:, 2] *= np.sign(fz_value)
    return mesh


def scale(mesh):
    bound_box = mesh.bounding_box
    smallest = max(bound_box.extents)
    scale = 1 / smallest

    scale_matrix = [[scale, 0, 0, 0],
                    [0, scale, 0, 0],
                    [0, 0, scale, 0],
                    [0, 0, 0, 1]]

    mesh.apply_transform(scale_matrix)
    return mesh


def normalization_tool(mesh):
    # Normalization of position
    mesh = position(mesh)
    # Alignment
    mesh, E, eigenvalues = alignment(mesh)
    # Flipping test
    mesh = orientation(mesh)
    # Normalization scale
    mesh = scale(mesh)
    return mesh, E, eigenvalues


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
            mesh = trimesh.load(filename, force='mesh')
            mesh, eigenvectors, eigenvalues = normalization_tool(mesh)
            triangles, quads = False, False
            type_of_faces = ''
            with open(filename) as f:
                num_line = 1
                for line in f.readlines():
                    if num_line == 2:
                        second_line = line
                    if line[:2] == '3 ':
                        triangles = True
                    elif line[:2] == '4 ':
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

                p1 = np.array([mesh.center_mass[0], mesh.center_mass[1], mesh.center_mass[2]])
                p2 = np.array([0, 0, 0])
                dist = distance_two_point(p1, p2)

                # Append the necessary info to variables for histograms
                vertice_nums.append(int(num_vert))
                category_nums.append(str(dir))
                faces_nums.append(int(num_faces))
                norm_dist.append(dist)
                long_boundbox.append(round(float(max(mesh.bounding_box.extents)), 5))

            eccentricity = eigenvalues[0] / eigenvalues[2]

            new_dict = {"shape_class": str(dir),
                        "num_verticles": int(num_vert),
                        "num_faces": int(num_faces),
                        "faces_type": str(type_of_faces),
                        "axis_bound_box": mesh.bounding_box.extents,
                        "bound_box": mesh.bounding_box_oriented.extents,
                        "path": filename,
                        "watertight": bool(mesh.is_watertight),
                        "area": float(mesh.area),
                        "volume": abs(float(mesh.volume)),
                        "compactness": float((mesh.area ** 3) / (36 * np.pi * ((abs(float(mesh.volume))) ** 2))),
                        "diameter": float(diameter2(mesh)),
                        "eccentricity": eccentricity,
                        "bound_box_volume": mesh.bounding_box_oriented.volume,
                        "a3": get_entries_from_histograms(mesh, "a3", 46),
                        "d1": get_entries_from_histograms(mesh, "d1", 1000),
                        "d2": get_entries_from_histograms(mesh, "d2", 100),
                        "d3": get_entries_from_histograms(mesh, "d3", 46),
                        "d4": get_entries_from_histograms(mesh, "d4", 26)
                        }
            output.append(new_dict)
            i += 1
    print(f"Number of 3D objects in dataset: {i}")
    return output


def get_entries_from_histograms(mesh, descriptor, n):
    if descriptor == "a3":
        values = fe.a3_values(mesh, n)
    elif descriptor == "d1":
        values = fe.d1_values(mesh, n)
    elif descriptor == "d2":
        values = fe.d2_values(mesh, n)
    elif descriptor == "d3":
        values = fe.d3_values(mesh, n)
    elif descriptor == "d4":
        values = fe.d4_values(mesh, n)
    fig, axs = plt.subplots(figsize=(10, 5))
    freq, bins, patches = axs.hist(values, bins=10, rwidth=0.8, color='dodgerblue', edgecolor='white')
    # for f, b0, b1 in zip(freq, bins[:-1], bins[1:]):
        # print(f'Bin {b0:.3f},{b1:.3f}: {f:.0f} entries')
    return freq


def diameter2(mesh):
    vertices = mesh.vertices
    hull = ConvexHull(vertices)
    hullpoints = vertices[hull.vertices, :]
    hdist = cdist(hullpoints, hullpoints, metric='euclidean')
    bestpair = np.unravel_index(hdist.argmax(), hdist.shape)
    diam = distance_two_point(hullpoints[bestpair[0]], hullpoints[bestpair[1]])
    return diam


def distance_two_point(p1, p2):
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


def save_excel(folder, new_file):
    out = save_ouput(folder)
    df = pd.DataFrame.from_dict(out)
    df.to_excel(new_file)


def show_global_descrip_examples():
    # Examples for area descriptor
    mesh = trimesh.load("LabeledDB_new/Glasses/52.off", force='mesh')
    mesh.show()
    mesh = trimesh.load("LabeledDB_new/Cup/37.off", force='mesh')
    mesh.show()

    # Examples for volume descriptor
    mesh = trimesh.load("LabeledDB_new/Glasses/53.off", force='mesh')
    mesh.show()
    mesh = trimesh.load("LabeledDB_new/Mech/334.off", force='mesh')
    mesh.show()

    # Examples for compactness descriptor
    mesh = trimesh.load("LabeledDB_new/Vase/368.off", force='mesh')
    mesh.show()
    mesh = trimesh.load("LabeledDB_new/Cup/39.off", force='mesh')
    mesh.show()

    # Examples for diameter descriptor
    mesh = trimesh.load("LabeledDB_new/Bird/252.off", force='mesh')
    mesh.show()
    mesh = trimesh.load("LabeledDB_new/Mech/340.off", force='mesh')
    mesh.show()

    # Examples for eccentricity descriptor
    # mesh = trimesh.load("LabeledDB_new/Vase/368.off", force='mesh')
    # mesh.show()
    # mesh = trimesh.load("LabeledDB_new/Cup/158.off", force='mesh')
    # mesh.show()

    # Examples for AABB box volume descriptor
    mesh = trimesh.load("LabeledDB_new/Glasses/47.off", force='mesh')
    mesh.show()
    mesh = trimesh.load("LabeledDB_new/Table/145.off", force='mesh')
    mesh.show()


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
                    [0, 0, 0, 1]]

    mesh.apply_transform(scale_matrix)
    print(mesh.bounding_box.extents)
    (mesh + mesh2).show()


# # uncomment the line below to save the excel file
save_excel(DIR, "descriptors.xlsx")


def proof_alignment(folder):
    cos_list, cos_list_new = [], []
    x_vector = np.array([1, 0, 0])
    for dir in tqdm(os.listdir(folder)):
        for filename in glob.iglob(f'{folder}/{dir}/*.off'):
            mesh = trimesh.load(filename, force='mesh')
            mesh = position(mesh)
            mesh, eigenvectors, eigenvalues = alignment(mesh)
            mesh, eigenvectors_new, eigenvalues_new = alignment(mesh)
            cos = abs(np.dot(eigenvectors[0], x_vector) / np.linalg.norm(eigenvectors[0]) / np.linalg.norm(x_vector))
            cos_list.append(cos)
            cos_new = abs(
                np.dot(eigenvectors_new[0], x_vector) / np.linalg.norm(eigenvectors_new[0]) / np.linalg.norm(x_vector))
            cos_list_new.append(cos_new)
    plt.hist(cos_list, rwidth=0.95, bins=15)
    plt.title('Cosine of angle between a major eigenvector and the X axis')
    plt.ylabel('frequency')
    plt.xlabel('cosine')
    plt.show()

    plt.hist(cos_list_new, rwidth=0.95, bins=15)
    plt.title('Cosine of angle between a new major eigenvector and the X axis')
    plt.ylabel('frequency')
    plt.xlabel('cosine')
    plt.show()

# def proof_orientation(folder):
#     x_list, y_list, z_list = [], [], []
#     x_new_list, y_new_list, z_new_list = [], [], []
#     for dir in tqdm(os.listdir(DIR)):
#         for filename in glob.iglob(f'{DIR}/{dir}/*.off'):
#             mesh = trimesh.load(filename, force='mesh')
#             mesh = position(mesh)
#             mesh = alignment(mesh)
#             ...
#
#     plt.hist(x_list, rwidth=0.95, bins=10)
#     plt.title('Distribution of center of mass (x coordinates) before flipping test')
#     plt.ylabel('frequency')
#     plt.xlabel('x coordinates')
#     plt.show()
#
#     plt.hist(y_list, rwidth=0.95, bins=10)
#     plt.title('Distribution of center of mass (y coordinates) before flipping test')
#     plt.ylabel('frequency')
#     plt.xlabel('y coordinates')
#     plt.show()
#
#     plt.hist(z_list, rwidth=0.95, bins=10)
#     plt.title('Distribution of center of mass (z coordinates) before flipping test')
#     plt.ylabel('frequency')
#     plt.xlabel('z coordinates')
#     plt.show()
#
#     plt.hist(x_new_list, rwidth=0.95, bins=10)
#     plt.title('Distribution of center of mass (x coordinates) after flipping test')
#     plt.ylabel('frequency')
#     plt.xlabel('x cooridnates')
#     plt.show()
#
#     plt.hist(y_new_list, rwidth=0.95, bins=10)
#     plt.title('Distribution of center of mass (y coordinates) after flipping test')
#     plt.ylabel('frequency')
#     plt.xlabel('y coordinates')
#     plt.show()
#
#     plt.hist(z_new_list, rwidth=0.95, bins=10)
#     plt.title('Distribution of center of mass (z coordinates) after flipping test')
#     plt.ylabel('frequency')
#     plt.xlabel('z coordinates')
#     plt.show()
