import pandas as pd
import numpy as np

FILE = "descriptors.xlsx"
NEW_FILE = "normalized.xlsx"


def get_single_hist_column(df, descriptor, index, div):
    return [(int(value.replace('[', '').replace(']', '').replace('.', '').split()[index]))/div for value in df[descriptor].to_numpy()]


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
    a3_1 = [value.replace('[', '').replace(']', '').replace('.', '').split()[0] for value in df['a3'].to_numpy()]

    new_df = pd.DataFrame({'path': df['path'].to_numpy(),
                           'area': area,
                           'volume': volume,
                           'compactness': compactness,
                           'diameter': diameter,
                           'eccentricity': eccentricity,
                           'a3-1': get_single_hist_column(df, "a3", 0, 46 ** 3),
                           'a3-2': get_single_hist_column(df, "a3", 1, 46 ** 3),
                           'a3-3': get_single_hist_column(df, "a3", 2, 46 ** 3),
                           'a3-4': get_single_hist_column(df, "a3", 3, 46 ** 3),
                           'a3-5': get_single_hist_column(df, "a3", 4, 46 ** 3),
                           'a3-6': get_single_hist_column(df, "a3", 5, 46 ** 3),
                           'a3-7': get_single_hist_column(df, "a3", 6, 46 ** 3),
                           'a3-8': get_single_hist_column(df, "a3", 7, 46 ** 3),
                           'a3-9': get_single_hist_column(df, "a3", 8, 46 ** 3),
                           'a3-10': get_single_hist_column(df, "a3", 9, 46 ** 3),
                           'd1-1': get_single_hist_column(df, "d1", 0, 1000),
                           'd1-2': get_single_hist_column(df, "d1", 1, 1000),
                           'd1-3': get_single_hist_column(df, "d1", 2, 1000),
                           'd1-4': get_single_hist_column(df, "d1", 3, 1000),
                           'd1-5': get_single_hist_column(df, "d1", 4, 1000),
                           'd1-6': get_single_hist_column(df, "d1", 5, 1000),
                           'd1-7': get_single_hist_column(df, "d1", 6, 1000),
                           'd1-8': get_single_hist_column(df, "d1", 7, 1000),
                           'd1-9': get_single_hist_column(df, "d1", 8, 1000),
                           'd1-10': get_single_hist_column(df, "d1", 9, 1000),
                           'd2-1': get_single_hist_column(df, "d2", 0, 10000),
                           'd2-2': get_single_hist_column(df, "d2", 1, 10000),
                           'd2-3': get_single_hist_column(df, "d2", 2, 10000),
                           'd2-4': get_single_hist_column(df, "d2", 3, 10000),
                           'd2-5': get_single_hist_column(df, "d2", 4, 10000),
                           'd2-6': get_single_hist_column(df, "d2", 5, 10000),
                           'd2-7': get_single_hist_column(df, "d2", 6, 10000),
                           'd2-8': get_single_hist_column(df, "d2", 7, 10000),
                           'd2-9': get_single_hist_column(df, "d2", 8, 10000),
                           'd2-10': get_single_hist_column(df, "d2", 9, 10000),
                           'd3-1': get_single_hist_column(df, "d3", 0, 46 ** 3),
                           'd3-2': get_single_hist_column(df, "d3", 1, 46 ** 3),
                           'd3-3': get_single_hist_column(df, "d3", 2, 46 ** 3),
                           'd3-4': get_single_hist_column(df, "d3", 3, 46 ** 3),
                           'd3-5': get_single_hist_column(df, "d3", 4, 46 ** 3),
                           'd3-6': get_single_hist_column(df, "d3", 5, 46 ** 3),
                           'd3-7': get_single_hist_column(df, "d3", 6, 46 ** 3),
                           'd3-8': get_single_hist_column(df, "d3", 7, 46 ** 3),
                           'd3-9': get_single_hist_column(df, "d3", 8, 46 ** 3),
                           'd3-10': get_single_hist_column(df, "d3", 9, 46 ** 3)})
    return new_df


def save_new_excel(excel_file, new_file):
    output = save_output(excel_file)
    df = pd.DataFrame.from_dict(output)
    df.to_excel(new_file)


save_new_excel(FILE, NEW_FILE)
