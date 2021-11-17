from __future__ import print_function

import re
import pandas as pd
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------------------------------------------------------------------------------------
# This file creates uses t-SNE to create a 2 dimensional graph based on the 45 dimensional features vectors.
# -----------------------------------------------------------------------------------------------------------


# Function that plots using t-SNE
def plot_tsne():
    df = pd.read_excel("normalized.xlsx")
    paths = df['path'].tolist()
    classes = []
    for path in paths:
        sub_str = re.findall(r"\/\w+\/", path)[0]
        class_name = sub_str[1: len(sub_str)-1]
        classes.append(class_name)

    df['class'] = classes

    df_numeric = df.drop(columns=['num', 'path', 'class'])

    m = TSNE(learning_rate=50)
    tsne_features = m.fit_transform(df_numeric)

    df['x'] = tsne_features[:,0]
    df['y'] = tsne_features[:,1]

    sns.scatterplot(x="x", y="y", hue='class', data=df)
    plt.show()


plot_tsne()