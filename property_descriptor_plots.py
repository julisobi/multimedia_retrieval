import scipy.stats as stats
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import trimesh
from tqdm import tqdm
import feature_extraction as fe

DIR = 'LabeledDB_new'

def normalize_histogram_vals(hist_vals):
    sample_amount = len(hist_vals)
    for index in range(len(hist_vals)):
        hist_vals[index] = hist_vals[index]/sample_amount
    return hist_vals


def show_plots(data):
    class_names = ["airplane", "ant", "armadillo", "bearing", "bird", "bust", "chair", "cup", "fish", "fourleg",
                   "glasses", "hand", "human", "mech", "octopus", "plier", "table", "teddy", "vase"]
    fig, axs = plt.subplots(4, 5)

    for i in range(19):
        class_meshes = data[i]
        y = i % 5
        x = int((i - y) / 5)

        for mesh in class_meshes:
            mesh = normalize_histogram_vals(mesh)
            density = stats.gaussian_kde(mesh)
            n, p, _ = plt.hist(mesh, histtype=u'step', density=True)
            axs[x, y].plot(p, density(p))

        axs[x, y].set_title(class_names[i])

    fig.tight_layout()
    plt.show()

data = []
for x in range(19):
    data.append([])

i = 0
for dir in tqdm(os.listdir(DIR)):
    for filename in glob.iglob(f'{DIR}/{dir}/*.off'):
        values = fe.save_values_a3(filename, 100)
        data[i].append(values)
    i = i + 1

show_plots(data)
