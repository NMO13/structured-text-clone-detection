from __future__ import print_function
import time
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import seaborn as sns

# X, y = fetch_openml("mnist_784", version=1, return_X_y=True, as_frame=False)
#
# print(X.shape, y.shape)
#
# feat_cols = [ 'pixel'+str(i) for i in range(X.shape[1]) ]
# df = pd.DataFrame(X,columns=feat_cols)
# df['y'] = y
# df['label'] = df['y'].apply(lambda i: str(i))
# X, y = None, None
# print('Size of the dataframe: {}'.format(df.shape))
#
# # For reproducability of the results
# np.random.seed(42)
# rndperm = np.random.permutation(df.shape[0])
#
# plt.gray()
# fig = plt.figure( figsize=(16,7) )
# for i in range(0,15):
#     ax = fig.add_subplot(3,5,i+1, title="Digit: {}".format(str(df.loc[rndperm[i],'label'])) )
#     ax.matshow(df.loc[rndperm[i],feat_cols].values.reshape((28,28)).astype(float))
# plt.show()
#
# pca = PCA(n_components=2)
# pca_result = pca.fit_transform(df[feat_cols].values)
# df['pca-one'] = pca_result[:,0]
# df['pca-two'] = pca_result[:,1]
# #df['pca-three'] = pca_result[:,2]
# print('Explained variation per principal component: {}'.format(pca.explained_variance_ratio_))
# plt.figure(figsize=(16,10))
# sns.scatterplot(
#     x="pca-one", y="pca-two",
#     hue="y",
#     palette=sns.color_palette("hls", 10),
#     data=df.loc[rndperm,:],
#     legend="full",
#     alpha=0.3
# )
# plt.show()

def calculate_pca(similarity_vectors):
    # import pathlib
    # import os
    # from src.dataloading import load_data
    # path = pathlib.Path(__file__).parent.resolve()
    # st_path = "../../../data"
    # onlyfiles = [os.path.join(path, st_path, f) for f in os.listdir(os.path.join(path, st_path)) if os.path.isfile(os.path.join(path, st_path, f))]
    #
    # X = []
    # y = []
    # for file in onlyfiles:
    #     X_, y_ = load_data(file)
    #     X.extend(X_)
    #     y.extend(y_)

    df = pd.DataFrame(similarity_vectors)
    pca = PCA()
    pca_result = pca.fit_transform(df)
    df['pca-one'] = pca_result[:,0]
    df['pca-two'] = pca_result[:,1]
    return df, pca.explained_variance_ratio_


if __name__ == "__main__":
    df, expl_ratio = calculate_pca()
    print('Explained variation per principal component: {}'.format(expl_ratio))
    plt.figure(figsize=(16, 10))
    sns.scatterplot(
        x="pca-one", y="pca-two",
        palette=sns.color_palette("hls", 10),
        data=df,
        legend="full",
        alpha=0.3
    )
    plt.show()