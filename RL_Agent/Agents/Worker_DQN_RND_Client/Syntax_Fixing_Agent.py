import copy
import math
import random

import numpy as np
from Environment.Environment import Game_Type
from RL_Agent.Agents.Utils.DQNWorker import DQNWorker
import os
from RL_Agent.Agents.Utils.RDN import RDN
from RL_Agent.State_Representation.State_Representation import State_Representation
class Syntax_Fixing_Agent:
    def __init__(self,agent_id,model_checkpoint_file,load,learning=True) -> None:
        # whether to update the q values or not
        self.learning = learning

        # q values
        # input size is representation + error + action value + error
        # output size is 1

        q_value_file = os.path.join(model_checkpoint_file,f"Q_value_{agent_id}.model")
        q_value_file_mem = os.path.join(model_checkpoint_file,f"Q_value_{agent_id}.mem")

        try:
            load = os.path.join(load,f"Q_value_{agent_id}.mem")
        except:
            pass
        
        server_host = "127.0.0.1"
        server_port = 1234
        self.action_Q_value = DQNWorker(State_Representation.size() + 5, 1, q_value_file, q_value_file_mem, f"syntax_fixing_action_{agent_id}", server_host, server_port, learning,load=load)
        self.rdn = RDN(State_Representation.size()+5,1000,q_value_file,q_value_file_mem,f"syntax_fixing_action_{agent_id}")
        self.epsilon = 0.6
        self.decay_rate = 0.9999

        self.last_state = None
        self.last_selected_action = None

        self.local_time_stamp = 0

        self.is_last_error = None
        self.agent_id = agent_id
        pass

    def get_next_action(self,current_state,representation_vector,explore):
        '''
            get next action based on the agent policy and update/or not based on learning parameter
        '''

        # available actions
        available_actions = current_state["actions"]

        # exploit or explore
        eps_random = random.random()
        best_q_value = None
        if explore and eps_random < self.epsilon:
            # explore
            action = random.randint(0,len(available_actions)-1)
            selected_action =  available_actions[action]
        else:
            # exploit
            # rank available action types and get highest
            actions= [(current_state["error"],current_action["action"],current_action["range"],current_action["type"]) for current_action in available_actions]
            best_action,best_state,best_q_value = self.get_best_action(actions,representation_vector)
            selected_action = {"action": best_action[0], "range":best_action[1], "type":best_action[2]}


        # update local time stamp 
        self.local_time_stamp += 1

        #update state and action
        self.last_state = representation_vector

        self.last_selected_action = selected_action
        self.is_last_error = current_state["error"]

        return selected_action,best_q_value 

    def get_best_action(self,actions,representation_vector):
        best_action = None
        best_action_value = None
        best_state = None

        for error,current_action, current_range, current_type in actions:
            # generate representation
            current_state = copy.deepcopy(representation_vector)
            current_state.append(int(error))
            current_state.append(current_action)
            current_state.extend(current_range)
            current_state.append(current_type)
            current_q_value = self.action_Q_value.get_Q_value(current_state)[0][0]
            if best_action_value == None or current_q_value > best_action_value:
                best_action = (current_action,current_range,current_type)
                best_action_value = current_q_value
                best_state = current_state
        assert(best_action != None and best_action_value != None and best_state != None)
        return best_action,best_state,best_action_value


    def reward(self,last_state_representation,last_action,error,reward,current_state,representation_vector,global_time_stamp):
        if self.last_state != None and self.last_selected_action != None:
            # # decay epsilon
            self.epsilon *= self.decay_rate
            if self.epsilon < 0.2:
                self.epsilon = 0.5


            # ---------action Q network---------
            # get last state q-value
            last_q_value = copy.deepcopy(last_state_representation)
            last_q_value.append(error)
            last_q_value.append(last_action["action"])
            last_q_value.extend(last_action["range"])
            last_q_value.append(last_action["type"])

            # get current state q-value
            if current_state["game"] == Game_Type.DONE:
                current_q_value = np.float32(reward)
            else:
                actions= [(current_state["error"],current_action["action"],current_action["range"],current_action["type"]) for current_action in current_state["actions"]]
                best_action,best_state,current_q_value = self.get_best_action(actions,representation_vector)

            # get interensic reward
            expon_state = np.exp(last_q_value)
            interensic_reward = min(abs(self.rdn.get_value(expon_state)),0.7)
            
            # cache interensic reward 
            self.rdn.cache(expon_state)
            results_file = open(os.path.join("stats_logs",f"rewards_RDN{self.agent_id}.stats"),"a")
            results_file.write(f"{reward+interensic_reward}\n")
            results_file.close()

            # cache them
            self.action_Q_value.cache(last_q_value,current_q_value.item(),reward+interensic_reward)

            

            return None
        else:
            return None


    def stable_sigmoid(x):

        if x >= 0:
            z = math.exp(-x)
            sig = 1 / (1 + z)
            return sig
        else:
            z = math.exp(x)
            sig = z / (1 + z)
            return sig