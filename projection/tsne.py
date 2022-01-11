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

    from sklearn.manifold import TSNE
    X_embedded = TSNE(n_components=2, init='random').fit_transform(np.array(flattened_files))
    z, y = X_embedded[:,0], X_embedded[:,1]
    fig, ax = plt.subplots()
    ax.scatter(z, y)

    for i, txt in enumerate(labels):
        ax.annotate(txt, (z[i], y[i]))

    plt.show()