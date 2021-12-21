import os
import numpy as np
from collections import defaultdict
from src.vector_generation import create_similarity_vector, create_occurrence_list
from os import listdir
from os.path import isfile, join
st_path = os.path.join(os.environ.get("DATA_PATH"))
onlyfiles = [join(st_path, f) for f in listdir(st_path) if isfile(join(st_path, f))]
print(onlyfiles)

def flatten(all_keys, files):
    transformed_files = []
    for file in files:
        flat = defaultdict(lambda: 0)
        for k, v in file.items():
            for k1, v1 in v.items():
                key = "{}_{}".format(k, k1)
                all_keys.append(key)
                flat[key] += v1
        transformed_files.append(flat)
    return transformed_files

def annotate_missing_keys(flattened_files, all_keys):
    for file in flattened_files:
        for k in all_keys:
            if k not in file:
                file[k] = 0

def to_list(flattened_files):
    all = []
    for file in flattened_files:
        sortedKeys = sorted(file)
        all.append([file[k] for k in sortedKeys])
    return all

from src.ast_builder import ASTBuilder
creator = ASTBuilder()
l = []
all_keys = []
labels = []
for file in onlyfiles[:]:
    print("Parsing file {}".format(file))
    labels.append(file.split("/")[-1])
    with open(file) as f:
        tokens = creator.parse(f.read())
        l.append(create_occurrence_list(tokens))

flattened_files = flatten(all_keys, l)
all_keys = set(all_keys)
annotate_missing_keys(flattened_files, all_keys)
flattened_files = to_list(flattened_files)
print(flattened_files)

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(flattened_files)
explained_variance = pca.explained_variance_ratio_

z, y = principalComponents[:,0], principalComponents[:,1]
fig, ax = plt.subplots()
ax.scatter(z, y)

for i, txt in enumerate(labels):
    ax.annotate(txt, (z[i], y[i]))

plt.show()

from sklearn.manifold import TSNE
X_embedded = TSNE(n_components=2, learning_rate='auto',init='random').fit_transform(np.array(flattened_files))
z, y = X_embedded[:,0], X_embedded[:,1]
fig, ax = plt.subplots()
ax.scatter(z, y)

for i, txt in enumerate(labels):
    ax.annotate(txt, (z[i], y[i]))

plt.show()