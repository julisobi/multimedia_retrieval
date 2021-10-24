from pywebio.input import *
from pywebio.output import *
from os import listdir
from os.path import isfile, join
import random
import pandas as pd
import distances as dist

excel_file = "normalized.xlsx"
DIR = "LabeledDB_new"
categories = ["Airplane", "Ant", "Armadillo", "Bearing", "Bird", "Bust",
              "Chair", "Cup", "Fish", "FourLeg", "Glasses", "Hand", "Human",
              "Mech", "Octopus", "Plier", "Table", "Teddy", "Vase"]


def calculate_distances(vector, df, distance):
    distances = []
    rows = df.values.tolist()
    for row in rows:
        row[0] = row[0].replace("\\", "/")
        if distance == "eucl":
            distances.append((dist.euclidean_distance(vector, row[1:]), row[0]))
        elif distance == "cos":
            distances.append((dist.cosine_distance(vector, row[1:]), row[0]))
    return distances


def interface():
    put_text("This is the interface for the Multimedia Retrieval project")
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
        file_path = f"{path}\{file}"
        df = pd.read_excel(excel_file, index_col=0)
        row = df.loc[(df['path'] == file_path)]
        headers = list(row)[1:]
        values = df.loc[(df['path'] == file_path)].values[0][1:]
        put_table([headers, values])
        dist = calculate_distances(values, df, "cos")
        dist.sort(key=lambda tup: tup[0])
        put_table([('Distance', 'Path')] + dist)

    else:
        link = file_upload("Select a file:")
        print(link)


if __name__ == '__main__':
    interface()

