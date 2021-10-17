import scipy.stats as stats
import os
import numpy as np
import glob
import matplotlib.pyplot as plt
import trimesh
from tqdm import tqdm
import feature_extraction as fe

DIR = 'LabeledDB_new'


def showPlots(data):
    class_names = ["airplane", "ant", "armadillo", "bearing", "bird", "bust", "chair", "cup", "fish", "fourleg",
                   "glasses", "hand", "human", "mech", "octopus", "plier", "table", "teddy", "vase"]
    fig, axs = plt.subplots(4, 5)

    for i in range(19):
        class_meshes = data[i]
        y = i % 5
        x = int((i - y) / 5)

        for mesh in class_meshes:
            density = stats.gaussian_kde(mesh)
            n, p, _ = plt.hist(mesh, histtype=u'step', density=True)
            axs[x, y].plot(p, density(p))

        axs[x, y].set_title(class_names[i])

    fig.tight_layout()
    plt.show()

#data = [[[125, 251, 254, 221, 245, 257, 123, 215], [200, 220, 210, 200, 200, 200, 200, 150]], [[100, 600, 600, 500], [300, 310, 432, 343]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],[]]
#showPlots(data)


data = []
for x in range(19):
     data.append([])

i = 0
for dir in tqdm(os.listdir(DIR)):
   for filename in glob.iglob(f'{DIR}/{dir}/*.off'):
        values = fe.save_values_d2(filename, 5000)
        data[i].append(values)
   i = i + 1

showPlots(data)
