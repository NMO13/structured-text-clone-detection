import matplotlib.pyplot as plt
import numpy as np
from src.vector_generation import create_occurrence_list
from projection.base import *

def perform(files):
    from src.ast_builder import ASTBuilder
    creator = ASTBuilder()
    l = []
    all_keys = []
    labels = []
    for file in files[:]:
        print("Parsing file {}".format(file[0]))
        labels.append(file[0].split("/")[-1])
        tokens = creator.parse(file[1])
        l.append(create_occurrence_list(tokens))


    flattened_files = flatten(all_keys, l)
    all_keys = set(all_keys)
    annotate_missing_keys(flattened_files, all_keys)
    flattened_files = to_list(flattened_files)
    print(flattened_files)

    from sklearn.decomposition import PCA
    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(flattened_files)
    explained_variance = pca.explained_variance_ratio_

    z, y = principalComponents[:,0], principalComponents[:,1]
    fig, ax = plt.subplots()
    ax.scatter(z, y)

    for i, txt in enumerate(labels):
        ax.annotate(txt, (z[i], y[i]))

    plt.show()