# Coronavirus Prediction Flask Web Application

Flask Web Project, using Flask, Bootstrap, Flask-SQLAlchemy

Currently in Progress, working on Dashboard

## Deployment

Currently deployed on Heroku: [Coronavirus Flask App](https://coronavirus-prediction-hse.herokuapp.com/)

## Neural Network
![Training Loss Curve](curve.gif)

```
class Net(torch.nn.Module):
    def __init__(self, n_feature, n_hidden, n_output):
        super(Net, self).__init__()
        self.hidden = torch.nn.Linear(n_feature, n_hidden).to(device)
        self.hidden1 = torch.nn.Linear(n_hidden, 800).to(device)
        self.hidden2 = torch.nn.Linear(800, 500).to(device)
        self.hidden3 = torch.nn.Linear(500, n_hidden).to(device)  # hidden layer
        self.predict = torch.nn.Linear(n_hidden, n_output).to(device)   # output layer
```

Route to train and update weighs on Cases model: `/api/predict/cases`

Route to train and update weighs on Deaths model: `/api/predict/deaths`

Models located in folder: app/models

## Instructions to Setup :

* Clone this repository.
* Use `git clone https://github.com/yaiestura/coronavirus_prediction.git` to clone this repository  to your computer
* Install pip3 on your system by `sudo apt-get install python3-pip` if not already installed.
* Create a virtual environment by the name of **venv** `virtualenv venv`. Information in setting up virtualenv can be found [here](https://docs.python-guide.org/dev/virtualenvs/ "Pipenv & Virtual Environments").
* Activate your virtualenv by `source venv/bin/activate` script
* Execute a `pip3 install -r requirements.txt` command to install the required packages.

## Working :

* Open a terminal and enter `python3 run.py`
* Finally, go to `localhost:5000` to display the start page of application.
* Or you can just run a bash script `sudo bash deploy.sh`
