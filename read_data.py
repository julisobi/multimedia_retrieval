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
from normalization import normalization_tool

DIR = 'LabeledDB_new'
VOLUME = 'V1_141_chair.off'
trimesh.util.attach_to_log()


def view_mesh(file):
    print(f"File {file}")
    mesh = trimesh.load(file, force='mesh')
    mesh.show()


def save_ouput(fold):
    output = []
    i = 0
    vertice_nums = []
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


def plot_category_distribution():
    df = pd.read_excel("descriptors.xlsx")
    categories = df["shape_class"].tolist()
    # Distribution of amount of meshes in each class
    plt.hist(categories, rwidth=0.95, bins=19)
    plt.xticks(rotation=90)
    plt.title('Distribution of meshes over the different classes')
    plt.ylabel('amount of meshes')
    plt.xlabel('category')
    plt.show()


def distance_two_point(p1, p2):
    squared_dist = np.sum((p1 - p2) ** 2, axis=0)
    return np.sqrt(squared_dist)


def norm_position_plots():
    fold = 'LabeledDB_new'
    dist_before = []
    dist_after = []


    for dir in tqdm(os.listdir(fold)):
        for filename in glob.iglob(f'{fold}/{dir}/*.off'):
            mesh = trimesh.load(filename, force='mesh')
            p1 = np.array([mesh.center_mass[0], mesh.center_mass[1], mesh.center_mass[2]])
            p2 = np.array([0, 0, 0])
            dist = distance_two_point(p1, p2)
            dist_before.append(dist)

            mesh, eigenvectors, eigenvalues = normalization_tool(mesh)
            p1 = np.array([mesh.center_mass[0], mesh.center_mass[1], mesh.center_mass[2]])
            p2 = np.array([0, 0, 0])
            dist_new = distance_two_point(p1, p2)
            dist_after.append(dist_new)


    # Distribution of amount of vertices before preprocessing
    plt.hist(dist_before, rwidth=0.95, bins=15)
    plt.title('Distances between barycenter of meshes and the world origin, before normalization')
    plt.ylabel('frequency')
    plt.xlabel('distance to origin')
    plt.show()

    # Distribution of amount of vertices after preprocessing
    plt.hist(dist_after, rwidth=0.95, bins=15)
    plt.title('Distances between barycenter of meshes and the world origin, after normalization')
    plt.ylabel('frequency')
    plt.xlabel('distance to origin')
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
# save_excel(DIR, "descriptors.xlsx")
#norm_position_plots()