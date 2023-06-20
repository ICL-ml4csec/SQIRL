# --------------------------------Federated learning server--------------------------------
# store the global neural network and service the clients agents by average weighting all parameters and send the updated prameters.
# communication is done using sockets and data transmitted using pickle bytes.
import copy
import optparse
import os
import pickle
import socket
from _thread import *
import struct
import sys
import time
from RL_Agent.Agents.Utils.Neural_Network import WorkerNeuralNetwork
from RL_Agent.State_Representation.State_Representation import State_Representation
import threading
import re 
__barrier = 0
__finished_update = False
clients = None
mutex_1 = threading.Lock()
mutex_2 = threading.Lock()
mutex_3 = threading.Lock()
mutex_4 = threading.Lock()
mutex_5 = threading.Lock()
host = '127.0.0.1'
port = 1234
load_path = ''

save_file_model = os.path.join("stats_logs","domain_time",'Checkpoint_Worker_Server',"Q_value.model")
state_size = State_Representation.size()+5
action_size = 1
agents_paramters = []
neural_network = None

def set_clients(no_clients):
    global clients
    with mutex_5:
        clients = no_clients
def decrement_clients():
    global clients
    with mutex_5:
        clients -= 1

def get_clients():
    global clients
    with mutex_5:
        return clients

def increment_barrier():
    global __barrier
    with mutex_1:
        __barrier += 1

def reset_barrier():
    global __barrier
    with mutex_1:
        __barrier = 0

def get_barrier_value():
    global __barrier
    with mutex_1:
        return __barrier

def add_paramters(params):
    global agents_paramters
    with mutex_2:
        agents_paramters.append(params)

    

def send_msg(sock, msg):
    # Prefix each message with a 4-byte length (network byte order)
    msg = struct.pack('>I', len(msg)) + msg
    sock.sendall(msg)

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

def service_client(connection):
    global __barrier
    global __finished_update
    global neural_network
    global agents_paramters
    global save_file_model
    global load_path
    send_msg(connection,str.encode('ACK'))

    # check type of service
    data = recv_msg(connection)
    message = data.decode('utf-8')
    # if init 
    if "INIT" in message:
        # send current parameters
        save_file_model = re.sub('domain', message.split('INIT:')[-1], save_file_model)
        if not os.path.exists(save_file_model.split('Q_value.model')[0]):
            os.makedirs(save_file_model.split('Q_value.model')[0])
        init_parameters = pickle.dumps({'save_loc':save_file_model, 'load_loc': load_path,'network_parameters': neural_network.get_parameters()})
        send_msg(connection,init_parameters)

    # else if update parameters
    elif message =="UPDATE":
        data = recv_msg(connection)
        client_data = pickle.loads(data)
        __finished_update = False
        with mutex_3:
            increment_barrier()
            is_final_element = (get_barrier_value() == get_clients())
            add_paramters(client_data)

        # sensitive area
        # if final client call update parameter function
        if is_final_element:
            print(f"final client arrived: {get_barrier_value()}")
            # call update
            update_paramters()

        # else wait for all clients and update
        else:
            print(f"waiting for other clients before update current clients arrived: {get_barrier_value()}")
            # wait to final client arrive and update finishes
            while not __finished_update:
                pass

        # send current parameters
        network_parameters = pickle.dumps(neural_network.get_parameters())
        send_msg(connection,network_parameters)

    # exit
    elif message == "EXIT":
        assert(get_clients() != 0)
        decrement_clients()
        if get_clients() == 0:
            __finished_update = False
        send_msg(connection,str.encode('ACK'))
        connection.close()
        if get_clients() == 0:
            sys.exit()

    connection.close()

def update_paramters():
    global locked
    global __barrier
    global __finished_update
    global neural_network
    global agents_paramters    
    global save_file_model


    assert(len(agents_paramters) == get_clients())
    stored_data = copy.deepcopy(agents_paramters[0])
    # average all paramters
    for current_key in agents_paramters[0]:
        for current_model_index in range(len(agents_paramters)):
            if current_model_index == 0:
                stored_data[current_key] = agents_paramters[current_model_index][current_key]
            else:
                stored_data[current_key] = (stored_data[current_key] + agents_paramters[current_model_index][current_key])
        
        stored_data[current_key] /= get_clients()


    

    # save model
    neural_network.update_paramters(stored_data)
    neural_network.save_model(save_file_model)



    # remove agents parameters
    agents_paramters.clear()

    # clear the barrier
    reset_barrier()

    # unlock update pass
    __finished_update = True
    print("[Worker_Server->update param] param have been updated")


def accept_connections(ServerSocket):
    Client, address = ServerSocket.accept()
    print('[Worker Server->accept connections] Connected to: ' + address[0] + ':' + str(address[1]))
    start_new_thread(service_client, (Client, ))

if __name__ == "__main__":
    try:

        # get parameter how many clients
        parser = optparse.OptionParser()
        parser.add_option('-u', '--clients',
                action="store", dest="clients",
                help="number_of_clients", default=2)

        parser.add_option('--model_dir',
                action="store", dest="model_dir",
                help="Directory containing model checkpoints, if not set a new agent will begin training", default=None)

        options, args = parser.parse_args()

        # setup neural_network
        try:
            load_path = os.path.join(options.model_dir +'Q_value.model')
        except:
            #load_path = os.path.join(os.getcwd() + '/RL_Agent/pretrained_agents/Worker_DQN_RND_Server/Q_value.model')
            load_path = None
        neural_network = WorkerNeuralNetwork.load_model(load_path)
        if neural_network is None:
            print("No saved model. Initialise new Neural Network....")
            neural_network = WorkerNeuralNetwork(state_size, action_size)
        else:
            print(f'Loaded model: {load_path}')

        save_time = time.strftime("%Y-%m-%d_%H-%M-%S")
        #global save_file_model
        save_file_model = re.sub('time', f'{save_time}', save_file_model)
        
        #print(f'Model will be saved in {save_file_model}') 

        set_clients(int(options.clients))

        # initiat socket
        ServerSocket = socket.socket()
        try:
            ServerSocket.bind((host, port))
        except socket.error as e:
            print(str(e))

        print(f'[Worker Server] listing on {host}:{port}')
        ServerSocket.listen()

        # apply multithreading function to service client requests
        while True:
            accept_connections(ServerSocket)
    except Exception:
        ServerSocket.close()