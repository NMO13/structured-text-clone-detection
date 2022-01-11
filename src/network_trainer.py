import os
import numpy as np
from src.dataloading import load_data
from src.nn.network_functions import train_net, predict
from src.create_data import are_similarity_vectors_available


def train():
    print("Training neural network...")
    import pathlib
    path = pathlib.Path(__file__).parent.resolve()
    st_path = "../data"
    onlyfiles = [os.path.join(path, st_path, f) for f in os.listdir(os.path.join(path, st_path)) if os.path.isfile(os.path.join(path, st_path, f))]

    if not are_similarity_vectors_available():
        raise Exception("No similarity vectors found. Abort.")

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