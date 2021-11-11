import numpy as np

def load_data(filename):
    with open(filename, 'rb') as f:
        X = np.load(f)
        y = np.load(f)
        return X, y

def save_data(originalfile, X, y):
    # create directory "data" first
    import os
    filename = os.path.join(os.path.dirname(__file__), "../data/{}.npy".format(originalfile))
    if os.path.exists(filename):
        os.remove(filename)

    with open(filename, 'wb') as f:
        np.save(f, X)
        np.save(f, y)