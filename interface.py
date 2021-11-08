from functools import partial

import pywebio
import time
import trimesh
from pywebio.input import *
from pywebio.output import *
from os import listdir
from os.path import isfile, join
import random
import pandas as pd

import distances
from read_data import normalization_tool, diameter2, get_entries_from_histograms, view_mesh
import numpy as np


weights = []
weights.extend([0.04] * 5)  # weights of global descriptors
weights.extend([0.02] * 40)  # weights of property descriptors

excel_file = "normalized.xlsx"
DIR = "LabeledDB_new"
categories = ["Airplane", "Ant", "Armadillo", "Bearing", "Bird", "Bust",
              "Chair", "Cup", "Fish", "FourLeg", "Glasses", "Hand", "Human",
              "Mech", "Octopus", "Plier", "Table", "Teddy", "Vase"]


trimesh.util.attach_to_log()


def get_weights(gdw, pdw):
    weights = []
    weights.extend([gdw] * 5)  # weights of global descriptors
    weights.extend([pdw] * 40)  # weights of property descriptors
    return weights


def start_interface():
    #while True:
    put_text("This is the interface for the Multimedia Retrieval project - by J. Sobiczewska and A. Vermast")
    put_button("Restart and try another mesh", onclick=lambda: restart(), color='success', outline=True)
    interface()
    pywebio.session.hold()


def interface():
    with use_scope('B'):
        option = radio("Select a mesh:", ["Choose mesh from existing", "Upload your own mesh"])
        if option == "Choose mesh from existing":
            category = select("Select category:", categories)
            path = f"{DIR}/{category}"
            files = [f for f in listdir(path) if isfile(join(path, f)) & f.endswith(".off")]
            random_file = random.choice(files)
            files.append("Random")
            file = select("Select file:", files)
            if file == "Random":
                file = random_file
            file_path = f"{path}/{file}"
            df = pd.read_excel(excel_file, index_col=0)
            row = df.loc[(df['path'] == file_path)]
            headers = list(row)[1:]
            values = df.loc[(df['path'] == file_path)].values[0][1:]

            pywebio.output.clear('B')

            put_table([headers, values])
            number = input("Choose the number of best-matching shapes to show:")

            # Use the next two lines for without ANN
            # dist = distances.calculate_distances(values, df)
            # dist.sort(key=lambda tup: tup[0])

            # Use the next line for with ANN
            dist = distances.ann(df, file_path, 10, int(number)+1)

            new_dist = []
            for item in dist[1:int(number) + 1]:
                new_item = (item[0], item[1], put_button("Visualize mesh", onclick=partial(view_mesh, file=item[1]), color='success', outline=True))
                new_dist.append(new_item)
            put_table([('Distance', 'Path', 'Open View')] + new_dist[0:int(number)+1])
            while not next:
                time.sleep(1)

        else:
            file = file_upload("Select a file:")
            f = open('uploads/' + file['filename'], 'wb')
            f.write(file['content'])

            mesh = trimesh.load('uploads/' + file['filename'], force='mesh')
            mesh, eigenvectors, eigenvalues = normalization_tool(mesh)
            area = float(mesh.area)
            volume = abs(float(mesh.volume))
            compactness = float((mesh.area ** 3) / (36 * np.pi * (volume ** 2)))
            diameter = float(diameter2(mesh))
            eccentricity = eigenvalues[0] / eigenvalues[2]
            a3 = get_entries_from_histograms(mesh, "a3", 46)
            a3_normalized = [int(val) / 46**3 for val in a3]
            d1 = get_entries_from_histograms(mesh, "d1", 7000)
            d1_normalized = [int(val) / 7000 for val in d1]
            d2 = get_entries_from_histograms(mesh, "d2", 100)
            d2_normalized = [int(val) / 10000 for val in d2]
            d3 = get_entries_from_histograms(mesh, "d3", 46)
            d3_normalized = [int(val) / 46**3 for val in d3]
            values = [area, volume, compactness, diameter, eccentricity]
            values.extend(a3_normalized)
            values.extend(d1_normalized)
            values.extend(d2_normalized)
            values.extend(d3_normalized)
            headers = ['area', 'volume', 'compactness', 'diameter', 'eccentricity']

            pywebio.output.clear('B')

            df = pd.read_excel(excel_file, index_col=0)
            put_table([headers, values])
            number = input("Choose the number of best-matching shapes to show:")
            dist = distances.calculate_distances(values, df)
            dist.sort(key=lambda tup: tup[0])
            new_dist = []
            for item in dist[:int(number)]:
                new_item = (item[0], item[1], put_button("Visualize mesh", onclick=partial(view_mesh, file=item[1]), color='success', outline=True))
                new_dist.append(new_item)
            put_table([('Distance', 'Path', 'Open View')] + new_dist)


def restart():
    print('restart')
    pywebio.output.clear('B')
    interface()


if __name__ == '__main__':
    #pywebio.start_server(start_interface(), debug=True)
    start_interface()


