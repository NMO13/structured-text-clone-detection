import os
import numpy as np
from src.dataloading import load_data
from src.nn.network_functions import train_net, predict


def train():
    import pathlib
    path = pathlib.Path(__file__).parent.resolve()
    st_path = "../data"
    onlyfiles = [os.path.join(path, st_path, f) for f in os.listdir(os.path.join(path, st_path)) if os.path.isfile(os.path.join(path, st_path, f))]

    if len(onlyfiles) == 0:
        # similarity vectors don't exist so far
        # so create them first and try again
        from src.create_data import main
        main()
        onlyfiles = [os.path.join(path, st_path, f) for f in os.listdir(os.path.join(path, st_path)) if
                     os.path.isfile(os.path.join(path, st_path, f))]

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