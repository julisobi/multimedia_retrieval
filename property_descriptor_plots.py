import re
import scipy.stats as stats
import matplotlib.pyplot as plt
import pandas as pd
import json
import numpy as np


def normalize_histogram_vals(hist_vals):
    sample_amount = sum(hist_vals)
    for index in range(len(hist_vals)):
        hist_vals[index] = hist_vals[index] / sample_amount
    return hist_vals


def get_data_for_plot(descriptor: str):
    data_dict = pd.read_excel("filter2.xlsx", None)
    column_name = descriptor
    df = data_dict["Sheet1"]
    descriptor_data = df[column_name].values
    return descriptor_data


def total_plots_old(descriptor: str):
    data_dict = pd.read_excel("filter2.xlsx", None)
    df = data_dict["Sheet1"]
    descriptor_data = df[descriptor].tolist()

    class_names = ["airplane", "ant", "armadillo", "bearing", "bird", "bust", "chair", "cup", "fish", "fourleg",
                   "glasses", "hand", "human", "mech", "octopus", "plier", "table", "teddy", "vase"]
    fig, axs = plt.subplots(4, 5)

    for row_index in range(1, len(descriptor_data)):
        row_df = df.iloc[[row_index]]
        class_name = row_df["shape_class"].tolist()[0]
        class_index = class_names.index(class_name.lower())

        y = class_index % 5
        x = int((class_index - y) / 5)

        hist_values_cell = df.iloc[row_index][descriptor]
        # Somehow, it can only read the value in the Excel cell out as a string, so we use json to contert it back
        # into a list.
        hist_values = json.loads(hist_values_cell)
        density = stats.gaussian_kde(hist_values)
        n, p, _ = plt.hist(hist_values, histtype=u'step', density=True)
        axs[x, y].plot(p, density(p))

        axs[x, y].set_title(class_names[class_index])

    fig.tight_layout()
    plt.show()


def total_plots_new(descriptor: str):
    data_dict = pd.read_excel("descriptors.xlsx", None)
    df = data_dict["Sheet1"]
    descriptor_data = df[descriptor].tolist()

    class_names = ["airplane", "ant", "armadillo", "bearing", "bird", "bust", "chair", "cup", "fish", "fourleg",
                   "glasses", "hand", "human", "mech", "octopus", "plier", "table", "teddy", "vase"]
    fig, axs = plt.subplots(4, 5)

    for row_index in range(1, len(descriptor_data)):
        row_df = df.iloc[[row_index]]
        class_name = row_df["shape_class"].tolist()[0]
        class_index = class_names.index(class_name.lower())

        y = class_index % 5
        x = int((class_index - y) / 5)

        hist_values_cell = df.iloc[row_index][descriptor]
        # Somehow, it can only read the value in the Excel cell out as a string, which is a weird point separated
        # format, so I use regex to extract the numbers into a list.
        new = re.findall("\d+", hist_values_cell)
        plot_values = [int(x) for x in new]
        #plot_values = normalize_histogram_vals(plot_values)

        axs[x, y].plot(plot_values)
        #axs[x, y].set_xticks([2, 4, 6, 8, 10])
        axs[x, y].set_title(class_names[class_index])

    fig.tight_layout()

    plt.show()


# MAIN
# total_plots_new("a3")
total_plots_new("d1")
# total_plots_new("d2")
# total_plots_new("d3")
# total_plots_new("d4")
