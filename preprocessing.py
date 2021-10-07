import pymeshlab as ml
import os
import glob
import matplotlib.pyplot as plt
from shutil import copyfile
from tqdm import tqdm

DIR = 'LabeledDB_new'
NEW_DIR = 'output_meshes'


def save_output(fold):
    i = 0
    if not os.path.exists(NEW_DIR):
        os.makedirs(NEW_DIR)
    for dir in os.listdir(fold):
        for filename in glob.iglob(f'{fold}/{dir}/*.off'):
            filebasename = os.path.basename(filename)
            with open(filename) as f:
                line = f.readlines()[1]
                num_vert = line.split()[0]
                if int(num_vert) > 8000:
                    i += 1
                    copyfile(filename, f'{NEW_DIR}/subs_{dir}_{filebasename}')
                    print(filename)
                else:
                    copyfile(filename, f'{NEW_DIR}/{dir}_{filebasename}')
    print(f"{i} files ")


def subsampling(dir):
    TARGET = 8000
    num_faces = 100 + 2 * TARGET
    os.chdir(dir)
    for file in tqdm(glob.iglob('subs_*.off')):
        ms = ml.MeshSet()
        ms.load_new_mesh(file)
        while (ms.current_mesh().vertex_number() > TARGET):
            ms.apply_filter('simplification_quadric_edge_collapse_decimation', targetfacenum=num_faces,
                            preservenormal=True)
            num_faces = num_faces - (ms.current_mesh().vertex_number() - TARGET)

        ms.save_current_mesh(f'{file[5:]}')
        os.remove(file)


def new_histograms(dir):
    vertices, faces = [], []
    for file in os.listdir(dir):
        with open(f'{dir}/{file}') as f:
            line = f.readlines()[1]
            vertices.append(int(line.split()[0]))
            faces.append(int(line.split()[0]))

    # Distribution of amount of vertices after preprocessing
    plt.hist(vertices, rwidth=0.95, bins=15)
    plt.title('Distribution of amount of vertices')
    plt.ylabel('frequency')
    plt.xlabel('# of vertices')
    plt.show()

    # Distribution of amount of faces after preprocessing
    plt.hist(faces, rwidth=0.95, bins=15)
    plt.title('Distribution of amount of faces')
    plt.ylabel('frequency')
    plt.xlabel('# of faces')
    plt.show()


# save_output(DIR)
# subsampling(NEW_DIR)
new_histograms(NEW_DIR)

