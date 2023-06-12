import torch
from torch import nn, sigmoid
from torch.utils.data import DataLoader
import torch.nn as nn
import copy

# Get cpu or gpu device for training.
device = "cuda" if torch.cuda.is_available() else "cpu"

# Define model
class DQN_neural_network(nn.Module):
    #load saved model
    def load_model(path):
        try:
            return torch.load(path)
        except:
            print('No saved model found, starting from scratch...')
            return None

    #init new network
    def __init__(self,state_size,action_size):
        super(DQN_neural_network, self).__init__()

        self.online = nn.Sequential(
            nn.Linear(state_size, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),
        )

        self.target = copy.deepcopy(self.online)

        # Q_target parameters are frozen.
        for p in self.target.parameters():
            p.requires_grad = False


    def forward(self, input, model):

        if model == "online":
            return self.online(input)
        elif model == "target":
            return self.target(input)

class DRQN_neural_network(nn.Module):
    #load saved model
    def load_model(path):
        try:
            return torch.load(path)
        except:

            return None

    #init new network
    def __init__(self,state_size,action_size):
        super(DRQN_neural_network, self).__init__()
        self.state_size = state_size
        self.online_RNN = nn.GRU(state_size, 2048)
        self.online = nn.Sequential(
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),

        )
        self.target_RNN = copy.deepcopy(self.online_RNN)

        self.target = copy.deepcopy(self.online)

        # Q_target parameters are frozen.
        for p in self.target_RNN.parameters():
            p.requires_grad = False

        # Q_target parameters are frozen.
        for p in self.target.parameters():
            p.requires_grad = False

    def init_hidden(self):
        return torch.zeros(1, 2048, device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
    
    def forward(self, input, hidden,model):

        if hidden is None:
            hidden = self.init_hidden()

        if model == "online":
            output,hidden = self.online_RNN(input,hidden)

            return self.online(hidden),hidden.detach()

        elif model == "target":
            output,hidden = self.target_RNN(input,hidden)
            return self.target(hidden),hidden.detach()


class RDN_neural_network(nn.Module):
    #load saved model
    def load_model(path):
        try:
            return torch.load(path)
        except:

            return None

    #init new network
    def __init__(self,state_size,action_size):
        super(RDN_neural_network, self).__init__()

        self.online = nn.Sequential(
            nn.Linear(state_size, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),
        )

        self.target = nn.Sequential(
            nn.Linear(state_size, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),
        )

        # Q_target parameters are frozen.
        for p in self.target.parameters():
            p.requires_grad = False


    def forward(self, input, model):

        if model == "online":
            return self.online(input)
        elif model == "target":
            return self.target(input)

class RDN_neural_network_2(nn.Module):
    #load saved model
    def load_model(path):
        try:
            return torch.load(path)
        except:

            return None

    #init new network
    def __init__(self,state_size,action_size):
        super(RDN_neural_network, self).__init__()

        self.online = nn.Sequential(
            nn.Linear(state_size, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),
            nn.ReLU(),

        )

        self.target = nn.Sequential(
            nn.Linear(state_size, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),
            nn.ReLU(),

        )

        # Q_target parameters are frozen.
        for p in self.target.parameters():
            p.requires_grad = False


    def forward(self, input, model):

        if model == "online":
            return self.online(input)
        elif model == "target":
            return self.target(input)

class WorkerNeuralNetwork(nn.Module):
    #load saved model
    def load_model(path):
        try:
            return torch.load(path)
        except:

            return None
            
    def save_model(self,path):
        save_path = (
            path
        )
        torch.save(
            self,
            save_path
        )
    #init new network
    def __init__(self,state_size,action_size):
        super(WorkerNeuralNetwork, self).__init__()

        self.online = nn.Sequential(
            nn.Linear(state_size, 2048),
            nn.ReLU(),
            nn.Linear(2048, 1024),
            nn.ReLU(),
            nn.Linear(1024, 512),
            nn.ReLU(),
            nn.Linear(512, action_size),
        )

        self.target = copy.deepcopy(self.online)

        # Q_target parameters are frozen.
        for p in self.target.parameters():
            p.requires_grad = False


    def forward(self, input, model):

        if model == "online":
            return self.online(input)
        elif model == "target":
            return self.target(input)
    
    def get_parameters(self):
        return self.state_dict()

    def update_paramters(self,param):
        self.load_state_dict(param)