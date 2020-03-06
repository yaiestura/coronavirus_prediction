import operator
import json
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F

from app.data_parser.data_parser import *
torch.manual_seed(1)


class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden)
        self.hidden1 = torch.nn.Linear(n_hidden, 400)
        self.hidden2 = torch.nn.Linear(400, 300)
        self.hidden3 = torch.nn.Linear(300, n_hidden)  # hidden layer
        self.predict = torch.nn.Linear(n_hidden, n_output)   # output layer

    def forward(self, x):
        x = F.relu(self.hidden(x))      # activation function for hidden layer
        x = F.relu(self.hidden1(x))
        x = F.relu(self.hidden2(x))
        x = F.relu(self.hidden3(x))
        x = self.predict(x)             # linear output
        return x


def train_model(x, y, train):
    if not train:
        net = Net(n_feature=1, n_hidden=200, n_output=1)
        net.load_state_dict(torch.load('app/models/model1.pth', map_location='cpu'))
        net.eval()
        return net
    # my_images = []
    # fig, ax = plt.subplots(figsize=(12, 7))
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    x = torch.tensor(x).to(device).type(torch.cuda.FloatTensor)
    y = torch.tensor(y).to(device).type(torch.cuda.FloatTensor).unsqueeze(1)
    loss_func = torch.nn.MSELoss()
    net = Net(n_feature=1, n_hidden=200, n_output=1)
    net.train()
    net = net.to(device)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.0001)
    for t in range(2000):
        prediction = net(x)  # input x and predict based on x
        loss = loss_func(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    torch.save(net.state_dict(), 'app/models/model2.pth')
    return net


def plot_graph(model_name, x, y, y_pred):
    plt.scatter(x[:len(y)], y, s=10)
    sort_axis = operator.itemgetter(0)
    sorted_zip = sorted(zip(x, y_pred), key=sort_axis)
    x, y_pred = zip(*sorted_zip)

    plt.plot(x, y_pred, color='m')
    plt.title("Amount of " + model_name + " in each day")
    plt.xlabel("Day")
    plt.ylabel(model_name)
    plt.show()


def model_handler(training_set, train, days):
    x = np.arange(len(training_set[0])).reshape(-1, 1)
    y = np.asarray(training_set[1]).reshape(-1, 1)
    model = train_model(x, y, train)
    x1 = np.arange(len(training_set[0]) + days).reshape(-1, 1)
    result = torch.flatten(model(torch.tensor(x1).type(torch.FloatTensor))).tolist()
    return result


def start(days, train=False):
    cases = UpdatesDataParser().get_updates()['cases_plot']
    data = model_handler(cases, train, days)
    return data

