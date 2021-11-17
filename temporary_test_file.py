import trimesh
import os
import glob
import pandas as pd
from tqdm import tqdm

from normalization import normalization_tool

DIR = 'LabeledDB_new'


def save_ouput2(fold):
    output = []
    i = 0

    for dir in tqdm(os.listdir(fold)):
        for filename in glob.iglob(f'{fold}/{dir}/*.off'):
            mesh = trimesh.load(filename, force='mesh')
            vol_before = mesh.volume
            mesh, eigenvectors, eigenvalues = normalization_tool(mesh)
            type_of_faces = ''

            eccentricity = eigenvalues[0] / eigenvalues[2]

            new_dict = {"shape_class": str(dir),
                        "vol_before": vol_before,
                        "vol_after": float(mesh.volume),
                        "vol_after_abs": abs(float(mesh.volume))
                        }
            output.append(new_dict)
            i += 1
    print(f"Number of 3D objects in dataset: {i}")
    return output


def save_excel2(folder, new_file):
    out = save_ouput2(folder)
    df = pd.DataFrame.from_dict(out)
    df.to_excel(new_file)


save_excel2(DIR, "volumes.xlsx")