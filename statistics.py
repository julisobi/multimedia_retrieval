import matplotlib.pyplot as plt
import pandas as pd
from numpy import mean, quantile
from read_data import view_3d

excel_file = "filter.xlsx"


def get_list_from_excel(file):
    data = pd.read_excel(file)
    vertice_nums = list(data['num_verticles'])
    category_nums = list(data['shape_class'])
    faces_nums = list(data['num_faces'])
    return vertice_nums, category_nums, faces_nums


def show_plots(file):
    vertices, categories, faces = get_list_from_excel(file)

    # Distribution of amount of vertices before preprocessing
    plt.hist(vertices, rwidth=0.95, bins=15)
    plt.title('Distribution of amount of vertices')
    plt.ylabel('frequency')
    plt.xlabel('# of vertices')
    plt.show()

    # Distribution of different categories before preprocessing
    plt.hist(categories, rwidth=0.95, bins=19)
    plt.xticks(rotation=90)
    plt.title('Distribution of categories')
    plt.ylabel('frequency')
    plt.xlabel('category')
    plt.show()

    # Distribution of amount of faces before preprocessing
    plt.hist(faces, rwidth=0.95, bins=15)
    plt.title('Distribution of amount of faces')
    plt.ylabel('frequency')
    plt.xlabel('# of faces')
    plt.show()


def average_values(file):
    vertices, categories, faces = get_list_from_excel(file)
    mean_vert = round(mean(vertices))
    mean_faces = round(mean(faces))
    return mean_vert, mean_faces


def get_nearest_val(file):
    vertices, categories, faces = get_list_from_excel(file)
    mean_vert, mean_faces = average_values(file)
    diff_vert, diff_face = 10000, 10000
    nearest_vert, nearest_face = 0, 0
    v_index, f_index = 0, 0
    for i in range(len(vertices)):
        if abs(vertices[i] - mean_vert) < diff_vert:
            nearest_vert = vertices[i]
            diff_vert = abs(vertices[i] - mean_vert)
            v_index = i
        else:
            continue
    for j in range(len(faces)):
        if abs(faces[j] - mean_faces) < diff_face:
            nearest_face = faces[j]
            diff_face = abs(faces[j] - mean_faces)
            f_index = j
        else:
            continue
    return nearest_vert, v_index, diff_vert, nearest_face, f_index, diff_face


def get_outlier_val(file):
    vertices, categories, faces = get_list_from_excel(file)
    mean_vert, mean_faces = average_values(file)
    diff_vert, diff_face = 0, 0
    outl_vert, outl_face = 0, 0
    v_index, f_index = 0, 0
    for i in range(len(vertices)):
        if abs(vertices[i] - mean_vert) > diff_vert:
            outl_vert = vertices[i]
            diff_vert = abs(vertices[i] - mean_vert)
            v_index = i
        else:
            continue
    for j in range(len(faces)):
        if abs(faces[j] - mean_faces) > diff_face:
            outl_face = faces[j]
            diff_face = abs(faces[j] - mean_faces)
            f_index = j
        else:
            continue
    return outl_vert, v_index, diff_vert, outl_face, f_index, diff_face


def show_average_shape(file):
    data = pd.read_excel(file)
    paths = list(data['path'])
    nearest_vert, v_index, diff_vert, nearest_face, f_index, diff_face = get_nearest_val(file)
    if f_index == v_index:
        view_3d(paths[f_index])
    else:
        view_3d(paths[f_index])
        view_3d(paths[v_index])


def show_outlier_shape(file):
    data = pd.read_excel(file)
    paths = list(data['path'])
    outl_vert, v_index, diff_vert, outl_face, f_index, diff_face = get_outlier_val(file)
    if f_index == v_index:
        view_3d(paths[f_index])
    else:
        view_3d(paths[f_index])
        view_3d(paths[v_index])


def find_outliers(file):
    vertices, categories, faces = get_list_from_excel(file)
    data = pd.read_excel(file)
    paths = list(data['path'])
    outliers = []
    for i in range(len(vertices)):
        if vertices[i] < 100 or faces[i] < 100:
            outliers.append(paths[i])
    print(outliers)


def get_statistics(file):
    vertices, categories, faces = get_list_from_excel(file)
    mean_vert, mean_faces = average_values(file)
    print(f"Mean faces: {mean_faces}, Mean vertices: {mean_vert}")
    print(f"Q1 faces: {quantile(faces, .25)}, Q1 vertices: {quantile(vertices, .25)}")
    print(f"Q2 faces: {quantile(faces, .5)}, Q2 vertices: {quantile(vertices, .5)}")
    print(f"Q3 faces: {quantile(faces, .75)}, Q3 vertices: {quantile(vertices, .75)}")
    print(f"Min value faces: {min(faces)}, Min value vertices: {min(vertices)}")
    print(f"Max value faces: {max(faces)}, Max value vertices: {max(vertices)}")

# show_average_shape(excel_file)
# show_outlier_shape(excel_file)
# show_plots(excel_file)
# find_outliers(excel_file)
get_statistics(excel_file)
