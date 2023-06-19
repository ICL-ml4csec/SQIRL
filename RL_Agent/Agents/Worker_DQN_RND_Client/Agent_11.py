import pprint

from Environment.Environment import Game_Type
from RL_Agent.Agents.Worker_DQN_RND_Client.Syntax_Fixing_Agent import Syntax_Fixing_Agent
from RL_Agent.State_Representation.State_Representation import State_Representation
class Agent_11:
    actions= ["add_comma","add_comment","comment_range","add_paranthesis","add_quote","add_whitespace","add_string",\
          "add_and","add_or","add_if","add_sleep","add_union","add_where",\
          "capatilize_keyword","convert_str_char","convert_str_hex","convert_str_concat","change_non_whitespace",\
          "remove_token","convert AND to &", "add null byte to quote"]
    idx_to_action_map = {i:curr_action for i,curr_action in enumerate(actions)}
    action_to_idx_map = {curr_action:i for i,curr_action in enumerate(actions)}
    def __init__(self,agent_id,domain,learning=True,db_type="mysql") -> None:
        self.pp = pprint.PrettyPrinter(indent=4)

        self.syntax_fixing_agent = Syntax_Fixing_Agent(agent_id,domain,learning=learning)
        self.state_representation = State_Representation(db_type)
        self.last_game = None
        self.global_timestamp = 0
        self.reward_value = []
        self.last_state_representation = None
        self.last_state_action = None
        self.error = None
        pass

    def get_next_action(self,current_state,explore=True):
        '''
            return the action chosen by user
        '''


        #  current game
        current_game = current_state["game"]

        #  current payload
        current_payload = current_state["payload"]


        #  current sql statment
        current_sql = current_state["sql"]


        #  available actions
        available_actions = current_state["actions"]

        # generate representation
        representable_state = self.state_representation.represent_state(current_state["payload"],current_state["sql"],current_state["token"])

        # update timestamp
        self.global_timestamp += 1
        # map game to agent to get the action
       
        best_q_value = None
        if current_game == Game_Type.SYNTAX_FIXING or current_game == Game_Type.BEHAVIOR_CHANGING or current_game == Game_Type.SANITIZATION_ESCAPING:
            self.last_game = Game_Type.SYNTAX_FIXING
            action,best_q_value =  self.syntax_fixing_agent.get_next_action(current_state,representable_state,explore)
        else:

            action =  {"action":-1,"range":[-1,-1],"type":-1}

        
        
        self.last_state_action = action
        self.last_state_representation = representable_state
        self.error = current_state["error"]
        return action,best_q_value

    def reward(self,reward,current_state):


        # generate representation
        representable_state = self.state_representation.represent_state(current_state["payload"],current_state["sql"],current_state["token"])
        self.reward_value .append( reward)
        # map game to agent to reward agent
        
       
        if self.last_game == Game_Type.SYNTAX_FIXING or self.last_game == Game_Type.BEHAVIOR_CHANGING or self.last_game == Game_Type.SANITIZATION_ESCAPING:
                self.syntax_fixing_agent.reward(self.last_state_representation,self.last_state_action,self.error,reward,current_state,representable_state,self.global_timestamp)
        else:
                {}


        # tune all networks

        # syntax
        #print(self.syntax_fixing_agent.agent_id)
        loss_2_1 = self.syntax_fixing_agent.action_Q_value.tune_network(self.global_timestamp)

        # rdn
        self.syntax_fixing_agent.rdn.tune_network(self.global_timestamp)
        


  
        if self.last_game == Game_Type.SYNTAX_FIXING or self.last_game == Game_Type.BEHAVIOR_CHANGING or self.last_game == Game_Type.SANITIZATION_ESCAPING:
            return {Game_Type.SYNTAX_FIXING :[loss_2_1,0,0]}
        else:
            return {}