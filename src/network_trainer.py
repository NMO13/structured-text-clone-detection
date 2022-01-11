import os
import numpy as np
from src.dataloading import load_data
from src.nn.network_functions import train_net
from src.create_data import are_similarity_vectors_available, get_st_files


def train():
    print("Training neural network...")
    if not are_similarity_vectors_available():
        raise Exception("No similarity vectors found. Abort.")
    onlyfiles = get_st_files()

    X = []
    y = []
    for file in onlyfiles:
        X_, y_ = load_data(file)
        X.append(X_)
        y.append(y_)

    net = train_net(np.concatenate(X, axis=0), np.concatenate(y, axis=0))
    return net


if __name__ == "__main__":
    train()