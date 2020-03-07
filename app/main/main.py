import operator
import numpy as np
import matplotlib.pyplot as plt
import torch
from torch import cuda
import torch.nn.functional as F
import imageio

from app.data_parser.data_parser import *
torch.manual_seed(1)

use_cuda = torch.cuda.is_available()
if use_cuda:
    device = 'cuda:0'
    dtype = cuda.FloatTensor
    ltype = cuda.LongTensor
else:
    device = 'cpu'
    dtype = torch.FloatTensor
    ltype = torch.LongTensor


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


def train_model(x, y, train, flag):
    if not train:
        net = Net(n_feature=1, n_hidden=200, n_output=1)
        if flag == 'cases':
            net.load_state_dict(torch.load('app/models/cases.pth', map_location='cpu'))
        elif flag == 'deaths':
            net.load_state_dict(torch.load('app/models/deaths.pth', map_location='cpu'))
        net.eval()
        return net
    # my_images = []
    # fig, ax = plt.subplots(figsize=(12, 7))
    x = torch.tensor(x).to(device).type(dtype)
    if flag == 'deaths':
        y = torch.tensor(y).to(device).type(dtype)
    elif flag == 'cases':
        y = torch.tensor(y).to(device).type(dtype).unsqueeze(1)
    loss_func = torch.nn.MSELoss()
    net = Net(n_feature=1, n_hidden=200, n_output=1)
    net.train()
    net = net.to(device)
    optimizer = torch.optim.Adam(net.parameters(), lr=0.0002)
    for t in range(1800):
        prediction = net(x)  # input x and predict based on x
        loss = loss_func(prediction, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    #     plt.cla()
    #     ax.set_title('Regression Analysis', fontsize=35)
    #     ax.set_xlabel('Independent variable', fontsize=24)
    #     ax.set_ylabel('Dependent variable', fontsize=24)
    #     ax.scatter(x.cpu().data.numpy(), y.cpu().data.numpy(), color="orange")
    #     ax.plot(x.cpu().data.numpy(), prediction.cpu().data.numpy(), 'g-', lw=3)
    #     ax.text(1.0, 1, 'Step = %d' % t, fontdict={'size': 24, 'color': 'red'})
    #     ax.text(15, 1, 'Loss = %.4f' % loss.item(),
    #             fontdict={'size': 24, 'color': 'red'})
    #     fig.canvas.draw()  # draw the canvas, cache the renderer
    #     image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    #     image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    #
    #     my_images.append(image)
    #
    # # save images as a gif
    # imageio.mimsave('./curve_1.gif', my_images, fps=50)
    torch.save(net.state_dict(), 'app/models/' + flag + '.pth')
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


def model_handler(flag, training_set, train, days):
    x = np.arange(len(training_set[0])).reshape(-1, 1)
    y = np.asarray(training_set[1]).reshape(-1, 1).astype(np.int)
    model = train_model(x, y, train, flag)
    x1 = np.arange(len(training_set[0]) + days).reshape(-1, 1)
    result = torch.flatten(model(torch.tensor(x1).type(dtype))).tolist()
    return result


def start(in1, days, train=False):
    data = []
    if in1 == 'cases':
        cases = UpdatesDataParser().get_updates()['cases_plot']
        data = model_handler(in1, cases, train, days)
    elif in1 == 'deaths':
        d_all = np.asarray(DeathsDataParser().get_deaths()['total_deaths'])[:, :2]
        a = d_all[:, 0]
        b = d_all[:, 1]
        deaths = np.concatenate(([a], [b]), axis=0)
        data = model_handler(in1, deaths, train, days)
    return data
