import numpy as np

def load_data(filename):
    with open(filename, 'rb') as f:
        X = np.load(f)
        y = np.load(f)
        return X, y

def save_data(originalfile, X, y):
    import os
    filename = "../data/{}.npy".format(originalfile)
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'wb') as f:
        np.save(f, X)
        np.save(f, y)