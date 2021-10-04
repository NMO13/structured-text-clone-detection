import os
import numpy as np
from dataloading import load_data
from src.nn.network_functions import train_net, predict

def main():
    st_path = "../data"
    onlyfiles = [os.path.join(st_path, f) for f in os.listdir(st_path) if os.path.isfile(os.path.join(st_path, f))]

    X = []
    y = []
    for file in onlyfiles:
        X_, y_ = load_data(file)
        X.append(X_)
        y.append(y_)

    net = train_net(np.concatenate(X, axis=0), np.concatenate(y, axis=0))
    print(net)


if __name__ == "__main__":
    main()