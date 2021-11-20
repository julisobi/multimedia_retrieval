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

    m = TSNE(perplexity=30, learning_rate=50, n_iter=1000)
    # We tested different values for the parameters of TSNE:
    # Perplexity 20, 30 or 40?              (default is 30)
    # Learning rate 50, 100, 150, or 200    (default is 200)
    # Iterations 500, 1000 or 1500?         (default is 1000)

    tsne_features = m.fit_transform(df_numeric)

    df['x'] = tsne_features[:,0]
    df['y'] = tsne_features[:,1]

    sns.scatterplot(x="x", y="y", hue='class', data=df)
    plt.show()


plot_tsne()