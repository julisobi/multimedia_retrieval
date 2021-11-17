import numpy as np
import glob
import trimesh
import os
from tqdm import tqdm
import matplotlib.pyplot as plt

# -----------------------------------------------------------------------------------------------------------
# This file contains the functions responsible for normalizing the meshes.
# -----------------------------------------------------------------------------------------------------------


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


def position(mesh):
    translate_matrix = [[1, 0, 0, -mesh.center_mass[0]],
                        [0, 1, 0, -mesh.center_mass[1]],
                        [0, 0, 1, -mesh.center_mass[2]],
                        [0, 0, 0, 1]]
    mesh.apply_transform(translate_matrix)
    return mesh


def alignment(mesh):
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
