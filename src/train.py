import os
from dataloading import load_data
from src.nn.network_functions import train_net, predict

def main():
    st_path = "../data"
    onlyfiles = [os.path.join(st_path, f) for f in os.listdir(st_path) if os.path.isfile(os.path.join(st_path, f))]

    X, y = load_data(onlyfiles[0])
    net = train_net(X, y)
    print(net)


if __name__ == "__main__":
    main()