import time
from operator import index
import pprint
import random
class Agent_Random:
    actions= ["add_comma","add_comment","comment_range","add_paranthesis","add_quote","add_whitespace","add_string",\
          "add_and","add_or","add_if","add_sleep","add_union","add_where",\
          "capatilize_keyword","convert_str_char","convert_str_hex","convert_str_concat","change_non_whitespace",\
          "remove_token","convert AND to &", "add null byte to quote"]
    idx_to_action_map = {i:curr_action for i,curr_action in enumerate(actions)}
    action_to_idx_map = {curr_action:i for i,curr_action in enumerate(actions)}
    def __init__(self,learning=None) -> None:

        self.reward_value = []
        pass

    def get_next_action(self,current_state,learning=False):
        '''
            return the action chosen by user
        '''
        # print current game
        current_game = current_state["game"]

        # print current payload
        current_payload = current_state["payload"]


        # print current sql statment
        current_sql = current_state["sql"]


        # print available actions
        available_actions = current_state["actions"]
        action = random.randint(0, len(available_actions) - 1)
        selected_action = available_actions[action]
        if len(current_state['actions']) == 0:
            print(current_state)
            time.sleep(120)



        # return action
        return selected_action,1/len(Agent_Random.actions)

    def reward(self,reward,state):
        #print(reward)
        self.reward_value.append(reward)
        return {}