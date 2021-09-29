import torch
from torch import optim
from src.nn.network import NeuralNetwork
from torch.utils.data import Dataset, DataLoader

EPOCHS = 50
BATCH_SIZE = 64
LEARNING_RATE = 0.001

device = 'cuda' if torch.cuda.is_available() else 'cpu'
print('Using {} device'.format(device))


class TrainData(Dataset):

    def __init__(self, X_data, y_data):
        self.X_data = X_data
        self.y_data = y_data

    def __getitem__(self, index):
        return self.X_data[index], self.y_data[index]

    def __len__(self):
        return len(self.X_data)


def binary_acc(y_pred, y_test):
    y_pred_tag = torch.round(torch.sigmoid(y_pred))

    correct_results_sum = (y_pred_tag == y_test).sum().float()
    acc = correct_results_sum / y_test.shape[0]
    acc = torch.round(acc * 100)

    return acc

def train_net(X, y):
    net = NeuralNetwork()
    net.to(device)
    criterion = torch.nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(net.parameters(), lr=LEARNING_RATE)

    train_data = TrainData(torch.FloatTensor(X),
                           torch.FloatTensor(y))
    train_loader = DataLoader(dataset=train_data, batch_size=BATCH_SIZE, shuffle=True)
    net.train()
    for e in range(1, EPOCHS + 1):
        epoch_loss = 0
        epoch_acc = 0
        for X_batch, y_batch in train_loader:
            X_batch, y_batch = X_batch.to(device), y_batch.to(device)
            optimizer.zero_grad()

            y_pred = net(X_batch)

            loss = criterion(y_pred, y_batch.unsqueeze(1))
            acc = binary_acc(y_pred, y_batch.unsqueeze(1))

            loss.backward()
            optimizer.step()

            epoch_loss += loss.item()
            epoch_acc += acc.item()

        print(
            f'Epoch {e + 0:03}: | Loss: {epoch_loss / len(train_loader):.5f} | Acc: {epoch_acc / len(train_loader):.3f}')
    return net

def predict(net, sim_vector):
    return torch.sigmoid(net(torch.FloatTensor(sim_vector).to(device)))
