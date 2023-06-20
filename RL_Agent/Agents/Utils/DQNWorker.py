import os
import struct
import torch
import torch.optim as optim
import torch.nn.functional as F
import torch.nn as nn
import copy,datetime
from RL_Agent.Agents.Utils.Neural_Network import DQN_neural_network, WorkerNeuralNetwork
from pathlib import Path

from collections import deque
import numpy as np
import random
import pickle
from RL_Agent.Agents.Utils.Neural_Network import DQN_neural_network
import socket

# Get cpu or gpu device for training.
device = "cuda" if torch.cuda.is_available() else "cpu"
class DQNWorker:
    # server_host = '127.0.0.1'
    # server_port = 1234
    def __init__(self,state_size,action_size,name,server_host,server_port,domain,learning=True) -> None:
        self.learning = learning
        self.BATCH_SIZE = 512
        self.GAMMA = 1
        self.MEM_CAPACITY = 10000
        self.min_experiance = 20
        self.learn_every = 1  # no. of experiences between updates to Q_online
        self.sync_every = 20  # no. of experiences between Q_target & Q_online sync
        self.save_every = 100
        self.learning_rate = 0.00005
        self.name = name
        self.state_size = state_size
        self.action_size = action_size
        self.id = name.split('syntax_fixing_action_')[-1]
        self.Q_value, self.load_mem, self.save_dir_mem = DQNWorker.load_model(server_host, server_port, state_size, action_size, domain)
        self.server_host = server_host
        self.server_port = server_port
        self.load_mem = self.load_mem.replace('id', self.id)
        
        self.memory = DQNWorker.load_mem(self.load_mem)
        if self.memory is None:
            self.memory = deque(maxlen=self.MEM_CAPACITY)

        #if not os.path.exists(save_file_model):
        #    os.makedirs(save_file_model.split('Q_value.model')[0])

        self.optimizer = torch.optim.Adam(self.Q_value.parameters(), lr=self.learning_rate)
        self.loss_fn = torch.nn.SmoothL1Loss()
        self.save_dir_mem = self.save_dir_mem.replace('id', self.id)
        

        pass
    def send_msg(sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(sock):
        # Read message length and unpack it into an integer
        raw_msglen = DQNWorker.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return DQNWorker.recvall(sock, msglen)


    def recvall(sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = bytearray()
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def load_model(server_host,server_port,state_size,action_size,domain):
        # create new neural network
        q_value = WorkerNeuralNetwork(state_size, action_size)

        # connect to server
        ClientSocket = socket.socket()
        try:
            ClientSocket.connect((server_host, server_port))
        except socket.error as e:
            print(str(e))

        # get ack
        ack = DQNWorker.recv_msg(ClientSocket)
        ack = ack.decode('utf-8')
        if ack != "ACK":
            raise Exception(f"[DQN_Worker-> sync_Q_target] got responce {ack}, should be ACK")

        # send init command
        DQNWorker.send_msg(ClientSocket, str.encode(f"INIT:{domain}"))


        # get updated parameters
        init_parameter = DQNWorker.recv_msg(ClientSocket)
        init_parameter = pickle.loads(init_parameter)
        load_path = init_parameter['load_loc'] + f'/Q_value_id.mem' if  init_parameter['load_loc'] is not None else ''
        save_dir_mem = init_parameter['save_loc'].split('Q_value.model')[0] + 'Q_value_id.mem'
        server_paramters_loaded = init_parameter['network_parameters']

        # update online parameters
        q_value.update_paramters(server_paramters_loaded)

        # update target parameters
        # q_value.target.load_state_dict(q_value.online.state_dict())        
        ClientSocket.close()

        return q_value, load_path, save_dir_mem

    def save_mem(self,curr_step):
        with open(self.save_dir_mem,"wb") as f:
            pickle.dump(self.memory,f)


    def load_mem(path):
        try:
            with open(path,"rb") as f:
                data = pickle.load(f)

                return data
        except:
            return None

    def tune_network(self,curr_step):
        if curr_step % self.sync_every == 0:
            # send parameters to server and update with new parameters
            self.sync_Q_target()

        if curr_step % self.save_every == 0 and self.learning:
            self.save_mem(curr_step)

        if curr_step < self.min_experiance:
            return None

        


        # Sample from memory
        state, next_state, reward,size = self.recall()
        if state is None:
            return None
        # Get TD Estimate   
        td_est = self.td_estimate(state,size)
        

        # Get TD Target
        td_tgt = self.td_target(next_state, reward,size)


        

        # Backpropagate loss through Q_online
        loss = self.update_Q_online(td_est, td_tgt)

        return loss

    def get_Q_value(self,state):
        state = torch.tensor(state,dtype=torch.float32)
        state = state.unsqueeze(0)

        current_Q = self.Q_value(state, model="online")
        return current_Q.detach().numpy()

    def td_estimate(self, state,size):
        current_Q = self.Q_value(state, model="online")[
            np.arange(0, size)
        ]  # Q_online(s,a)

        return torch.max(current_Q,1)[0].unsqueeze(1)

    @torch.no_grad()
    def td_target(self, next_Q, reward,size):
        return (reward +self.GAMMA * next_Q).float()

    def update_Q_online(self, td_estimate, td_target):

        loss = self.loss_fn(td_estimate, td_target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()
        return loss.item()

    def sync_Q_target(self):
        # connect to server

        ClientSocket = socket.socket()
        try:
            ClientSocket.connect((self.server_host, self.server_port))
        except socket.error as e:
            print(str(e))

        # get ack
        ack = DQNWorker.recv_msg(ClientSocket)
        ack = ack.decode('utf-8')
        if ack != "ACK":
            raise Exception(f"[DQN_Worker-> sync_Q_target] got responce {ack}, should be ACK")

        # send update command
        DQNWorker.send_msg(ClientSocket, str.encode("UPDATE"))

        # send parameters
        DQNWorker.send_msg(ClientSocket, pickle.dumps(self.Q_value.get_parameters()))

        # get updated parameters
        server_paramters = DQNWorker.recv_msg(ClientSocket)
        server_paramters_loaded = pickle.loads(server_paramters)

        # update online parameters
        self.Q_value.update_paramters(server_paramters_loaded)

        # update target parameters
        self.Q_value.target.load_state_dict(self.Q_value.online.state_dict())
        ClientSocket.close()


    def cache(self, state, next_state, reward):
        """
        Store the experience to self.memory (replay buffer)

        Inputs:
        state (LazyFrame),
        next_state (LazyFrame),
        action (int),
        reward (float),
        done(bool))
        """

        state = torch.tensor(state,dtype=torch.float32)
        next_state = torch.tensor([next_state])
        reward = torch.tensor([reward])

        self.memory.append((state, next_state, reward))

    def recall(self):
        """
        Retrieve a batch of experiences from memory
        """
        size = min(self.BATCH_SIZE,len(self.memory))
        if size < 1:
            return None,None,None,None
        batch = random.sample(self.memory, size)
        state, next_state, reward = map(torch.stack, zip(*batch))
        return state, next_state, reward,size