import numpy as np
import random
import math
import trimesh
import matplotlib.pyplot as plt

FILE = "m107.off"
trimesh.util.attach_to_log()


def save_points(file):
    points = []
    with open(file) as f:
        for line in f.readlines()[2:]:
            if line[:2] not in ['3 ', '4 ']:
                line = [float(point) for point in line[:-1].split(' ')]
                points.append(line)
            else:
                break
    return points


def distance(p1, p2):
    squared_dist = np.sum((p1 - p2) ** 2, axis=0)
    dist = np.sqrt(squared_dist)
    return dist


def a1(file):
    points = save_points(file)
    random_p1 = np.array(random.choice(points))
    random_p2 = np.array(random.choice(points))
    random_p3 = np.array(random.choice(points))
    x1, y1, z1 = random_p1[0], random_p1[1], random_p1[2]
    x2, y2, z2 = random_p2[0], random_p2[1], random_p2[2]
    x3, y3, z3 = random_p3[0], random_p3[1], random_p3[2]
    num = (x2 - x1) * (x3 - x1) + (y2 - y1) * (y3 - y2) + (z2 - z1) * (z3 - z1)
    den = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) * \
          math.sqrt((x3 - x1) ** 2 + (y3 - y1) ** 2 + (z3 - z1) ** 2)
    angle = math.degrees(math.acos(num / den))
    return angle


def d1(file):
    mesh = trimesh.load(file, force='mesh')
    center = mesh.center_mass
    points = save_points(file)
    random_p = random.choice(points)
    dist = distance(center, random_p)
    return dist


def d2(file):
    points = save_points(file)
    random_p1 = np.array(random.choice(points))
    random_p2 = np.array(random.choice(points))
    dist = distance(random_p1, random_p2)
    return dist


def d3(file):
    points = save_points(file)
    random_p1 = np.array(random.choice(points))
    random_p2 = np.array(random.choice(points))
    random_p3 = np.array(random.choice(points))
    dist1 = distance(random_p1, random_p2)
    dist2 = distance(random_p2, random_p3)
    dist3 = distance(random_p1, random_p3)
    s = (dist1 + dist2 + dist3) / 2
    area = (s * (s - dist1) * (s - dist2) * (s - dist3)) ** 0.5
    sr = area ** 0.5
    return sr


def d4(file):
    points = save_points(file)
    random_p1 = np.array(random.choice(points))
    random_p2 = np.array(random.choice(points))
    random_p3 = np.array(random.choice(points))
    random_p4 = np.array(random.choice(points))
    ad = random_p1 - random_p4
    bd = random_p2 - random_p4
    cd = random_p3 - random_p4
    val = np.array([ad, bd, cd])
    abs_val = abs(np.linalg.det(val))
    volume = abs_val / 6
    cr = volume ** (1./3.)
    return cr


def save_values_a1(file, num_points):
    a1_val = []
    for i in range(num_points):
        new_val = a1(file)
        print(new_val)
        a1_val.append(new_val)
    return a1_val


def save_values_d1(file, num_points):
    d1_val = []
    for i in range(num_points):
        d1_val.append(d1(file))
    return d1_val


def save_values_d2(file, num_points):
    d2_val = []
    for i in range(num_points):
        d2_val.append(d2(file))
    return d2_val


def save_values_d3(file, num_points):
    d3_val = []
    for i in range(num_points):
        d3_val.append(d3(file))
    return d3_val


def save_values_d4(file, num_points):
    d4_val = []
    for i in range(num_points):
        d4_val.append(d4(file))
    return d4_val


def histograms(file, num_points):
    # a1 = save_values_a1(file, num_points)
    d1, d2, d3, d4 = save_values_d1(file, num_points), save_values_d2(file, num_points), \
                     save_values_d3(file, num_points), save_values_d4(file, num_points)

    # plt.hist(a1, rwidth=0.95)
    # plt.title('Distribution of a1 values')
    # plt.ylabel('frequency')
    # plt.xlabel('value')
    # plt.show()

    plt.hist(d1, rwidth=0.95)
    plt.xticks(rotation=90)
    plt.title('Distribution of d1 values')
    plt.ylabel('frequency')
    plt.xlabel('value')
    plt.show()

    plt.hist(d2, rwidth=0.95)
    plt.title('Distribution of d2 values')
    plt.ylabel('frequency')
    plt.xlabel('value')
    plt.show()

    plt.hist(d3, rwidth=0.95)
    plt.title('Distribution of d3 values')
    plt.ylabel('frequency')
    plt.xlabel('value')
    plt.show()

    plt.hist(d4, rwidth=0.95)
    plt.title('Distribution of d4 values')
    plt.ylabel('frequency')
    plt.xlabel('value')
    plt.show()


histograms(FILE, 100)
