import pymeshlab as ml
import os
import glob
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
                if int(num_vert) > 10000:
                    i += 1
                    copyfile(filename, f'{NEW_DIR}/subs_{dir}_{filebasename}')
                else:
                    copyfile(filename, f'{NEW_DIR}/{dir}_{filebasename}')
    print(f"{i} files ")


def remesh(dir):
    TARGET = 10000
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


save_output(DIR)
remesh(NEW_DIR)
