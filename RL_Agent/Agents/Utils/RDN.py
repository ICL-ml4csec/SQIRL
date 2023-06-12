import os
import torch
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn
import copy,datetime
from RL_Agent.Agents.Utils.Neural_Network import RDN_neural_network
from pathlib import Path

from collections import deque
import numpy as np
import random
import pickle
from RL_Agent.Agents.Utils.Neural_Network import DQN_neural_network
# Get cpu or gpu device for training.
device = "cuda" if torch.cuda.is_available() else "cpu"
class RDN:
    def __init__(self,state_size,action_size,save_file_model,save_file_mem,name) -> None:
        self.BATCH_SIZE = 512
        self.GAMMA = 1
        self.MEM_CAPACITY = 10000
        self.min_experiance = 20
        self.learn_every = 1  # no. of experiences between updates to Q_online
        self.sync_every = 400  # no. of experiences between Q_target & Q_online sync
        self.save_every = 100
        self.learning_rate = 0.00005
        self.name = name
       
        self.Q_value = RDN_neural_network(state_size,action_size)

       
        self.memory = deque(maxlen=self.MEM_CAPACITY)

        self.optimizer = torch.optim.Adam(self.Q_value.parameters(), lr=self.learning_rate)
        self.loss_fn = torch.nn.SmoothL1Loss()
        self.save_dir_model = save_file_model
        self.save_dir_mem = save_file_mem

        pass



    def tune_network(self,curr_step):

        
        # Sample from memory
        state,size = self.recall()
        if state is None:
            return None


        # Get TD Estimate   
        td_est = self.td_estimate(state,size)
        
        # Get TD Target
        td_tgt = self.td_target(state,size)
        
        # Backpropagate loss through Q_online
        loss = self.update_Q_online(td_est, td_tgt)

        return loss

    def get_value(self,state):
        state = torch.tensor(state,dtype=torch.float32)
        state = state.unsqueeze(0)


        current_Q = self.Q_value(state, model="online")

        current_Q_secound = self.Q_value(state, model="target")

        loss = self.loss_fn(current_Q, current_Q_secound)
        return loss.detach().numpy()

    def td_estimate(self, state,size):
        current_Q = self.Q_value(state, model="online")
        return current_Q

    @torch.no_grad()
    def td_target(self, state, size):
        
        current_Q = self.Q_value(state, model="target")
        return current_Q

    def update_Q_online(self, td_estimate, td_target):

        loss = self.loss_fn(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()


    def cache(self, state):
        """
        Store the experience to self.memory (replay buffer)

        Inputs:
        state (LazyFrame),
        """

        state = torch.tensor(state,dtype=torch.float32)
       

        self.memory.append((state))

    def recall(self):
        """
        Retrieve a batch of experiences from memory
        """
        size = min(self.BATCH_SIZE,len(self.memory))
        if size < 1:
            return None,None,None,None
        batch = random.sample(self.memory, size)[0]

        return batch,size