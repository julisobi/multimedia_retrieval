import matplotlib.pyplot as plt
import pandas as pd

excel_file = "filter.xlsx"


def show_plots(file):
    data = pd.read_excel(file)
    vertice_nums = list(data['num_verticles'])
    category_nums = list(data['shape_class'])
    faces_nums = list(data['num_faces'])

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


show_plots(excel_file)
