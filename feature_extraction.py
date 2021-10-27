import numpy as np
import random
import trimesh
import math

FILE = "m107.off"
trimesh.util.attach_to_log()


def distance(p1, p2):
    squared_dist = np.sum((p1 - p2) ** 2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist


def a3(points): 
    # random_points = random.sample(list(points), 3)
    # ba = np.array(random_points[0]) - np.array(random_points[1])
    # bc = np.array(random_points[2]) - np.array(random_points[1])
    random.shuffle(points)
    idx = random.sample(range(len(points)), 3)
    ba = np.array(points[idx[0]]) - np.array(points[idx[1]])
    bc = np.array(points[idx[2]]) - np.array(points[idx[1]])
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)


def d1(points, center):
    random.shuffle(points)
    idx = random.choice(range(len(points)))
    # random_p = random.choice(list(points))
    random_p = points[idx]
    return distance(np.array(center), np.array(random_p))


def d2(points):
    random.shuffle(points)
    idx = random.sample(range(len(points)), 2)
    # random_points = random.sample(list(points), 2)
    dist = distance(np.array(points[idx[0]]), np.array(points[idx[1]]))
    return dist


def d3(points):
    # random_points = random.sample(list(points), 3)
    random.shuffle(points)
    idx = random.sample(range(len(points)), 3)
    dist1 = distance(np.array(points[idx[0]]), np.array(points[idx[1]]))
    dist2 = distance(np.array(points[idx[1]]), np.array(points[idx[2]]))
    dist3 = distance(np.array(points[idx[0]]), np.array(points[idx[2]]))
    s = (dist1 + dist2 + dist3) / 2
    area = math.sqrt(s * (s - dist1) * (s - dist2) * (s - dist3))
    return area


def d4(points):
    # random_points = random.sample(list(points), 4)
    random.shuffle(points)
    idx = random.sample(range(len(points)), 4)
    ad = np.array(points[idx[0]]) - np.array(points[idx[3]])
    bd = np.array(points[idx[1]]) - np.array(points[idx[3]])
    cd = np.array(points[idx[2]]) - np.array(points[idx[3]])
    val = np.array([ad, bd, cd])
    abs_val = abs(np.linalg.det(val))
    volume = abs_val / 6
    cr = volume ** (1./3.)
    return cr


def save_values_a3(mesh, num_points):
    a3_val = []
    points = list(mesh.vertices)
    for i in range(num_points):
        a3_val.append(a3(points))
    return a3_val


def save_values_d1(mesh, num_points):
    d1_val = []
    center = mesh.center_mass
    points = list(mesh.vertices)
    for i in range(num_points):
        d1_val.append(d1(points, center))
    return d1_val


def save_values_d2(mesh, num_points):
    d2_val = []
    points = list(mesh.vertices)
    for i in range(num_points):
        d2_val.append(d2(points))
    return d2_val


def save_values_d3(mesh, num_points):
    d3_val = []
    points = list(mesh.vertices)
    for i in range(num_points):
        d3_val.append(d3(points))
    return d3_val


def save_values_d4(mesh, num_points):
    d4_val = []
    points = list(mesh.vertices)
    for i in range(num_points):
        d4_val.append(d4(points))
    return d4_val
