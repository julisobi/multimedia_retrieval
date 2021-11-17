import numpy as np

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