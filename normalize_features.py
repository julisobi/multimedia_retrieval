import pandas as pd
import numpy as np

FILE = "filter.xlsx"
NEW_FILE = "normalized.xlsx"


def normalize_single_feature(list_of_f):
    standardized = []
    mean = np.mean(list_of_f)
    std = np.std(list_of_f)
    for i in range(len(list_of_f)):
        standardized.append((list_of_f[i] - mean)/std)
    return standardized


def save_output(excel_file):
    df = pd.read_excel(excel_file, index_col=0)
    area = normalize_single_feature(df['area'].to_numpy())
    volume = normalize_single_feature(df['volume'].to_numpy())
    compactness = normalize_single_feature(df['compactness'].to_numpy())
    diameter = normalize_single_feature(df['diameter'].to_numpy())
    eccentricity = normalize_single_feature(df['eccentricity'].to_numpy())
    new_df = pd.DataFrame({'path': df['path'].to_numpy(),
                           'area': area,
                           'volume': volume,
                           'compactness': compactness,
                           'diameter': diameter,
                           'eccentricity': eccentricity})
    return new_df


def save_new_excel(excel_file, new_file):
    output = save_output(excel_file)
    df = pd.DataFrame.from_dict(output)
    df.to_excel(new_file)


save_new_excel(FILE, NEW_FILE)
