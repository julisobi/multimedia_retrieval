import pywebio
import time
import trimesh
from pywebio.input import *
from pywebio.output import *
from os import listdir
from os.path import isfile, join
import random
import pandas as pd

import distances as dist
from read_data import normalization_tool, diameter2
import numpy as np


weights = []
weights.extend([0.04] * 5)  # weights of global descriptors
weights.extend([0.02] * 40)  # weights of property descriptors

excel_file = "normalized.xlsx"
DIR = "LabeledDB_new"
categories = ["Airplane", "Ant", "Armadillo", "Bearing", "Bird", "Bust",
              "Chair", "Cup", "Fish", "FourLeg", "Glasses", "Hand", "Human",
              "Mech", "Octopus", "Plier", "Table", "Teddy", "Vase"]


def get_weights(gdw, pdw):
    weights = []
    weights.extend([gdw] * 5)  # weights of global descriptors
    weights.extend([pdw] * 40)  # weights of property descriptors
    return weights


def calculate_distances(vector, df, distance):
    distances = []
    rows = df.values.tolist()
    weights = get_weights(0.04, 0.02)
    for row in rows:
        row[0] = row[0].replace("\\", "/")
        if distance == "eucl":
            distances.append((dist.euclidean_distance(vector, row[1:], weights), row[0]))
        elif distance == "cos":
            distances.append((dist.cosine_distance(vector, row[1:], weights), row[0]))
        elif distance == "emd":
            distances.append((dist.earth_movers_distance(vector, row[1:], weights), row[0]))
    return distances


def start_interface():
    #while True:
    put_text("This is the interface for the Multimedia Retrieval project")
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
            dist = calculate_distances(values, df, "emd")
            dist.sort(key=lambda tup: tup[0])
            put_table([('Distance', 'Path')] + dist[1:int(number)+1])
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
            values = [area, volume, compactness, diameter, eccentricity]
            headers = ['area', 'volume', 'compactness', 'diameter', 'eccentricity']

            pywebio.output.clear('B')

            put_table([headers, values])
            df = pd.read_excel(excel_file, index_col=0)
            dist = calculate_distances(values, df, "cos")
            dist.sort(key=lambda tup: tup[0])
            put_table([('Distance', 'Path')] + dist)


def restart():
    print('restart')
    pywebio.output.clear('B')
    interface()


if __name__ == '__main__':
    #pywebio.start_server(start_interface(), debug=True)
    start_interface()


