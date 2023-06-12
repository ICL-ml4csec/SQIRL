from enum import Enum
import sys

from Environment.Input.Crawler import Crawler
from Environment.Input_Storage import Input_storage
from Environment.SQL.SQL_Filter import SQL_Filter
from Environment.SQL.SQL_Filter_Worker import SQL_Filter_Worker
from Environment.Tokens_Actions.Basic_Block.Token import Token

class Game_Type(Enum):
    BEHAVIOR_CHANGING = 1
    SYNTAX_FIXING = 2
    SANITIZATION_ESCAPING = 3
    DONE = 4
    def __str__(self) -> str:
        return self._name_
    def __repr__(self) -> str:
        return super().__str__()
class SQLI_Environment:
    game_to_token = {Game_Type.BEHAVIOR_CHANGING:[Token.Category.BEHAVIOR_CHANGING], Game_Type.SYNTAX_FIXING:[Token.Category.BASIC_BLOCK,Token.Category.SYNTAX_FIXING], Game_Type.SANITIZATION_ESCAPING:[Token.Category.SANATISATION_ESCAPING], Game_Type.DONE:[]}
    
    def __init__(self,is_end_to_end,is_federated,crawler_input:tuple,sql_proxy_input:tuple,input_selection,verbose=0) -> None:
        self.__input_storage = Input_storage()
        assert(len(crawler_input) == 2)
        self.__crawler = Crawler(crawler_input[1],verbose)
        assert(len(sql_proxy_input) == 2)
        if is_federated:
            self.__sql_filter = SQL_Filter_Worker(*sql_proxy_input)
        else:  
            self.__sql_filter = SQL_Filter(*sql_proxy_input)
        self.setup_inputs(crawler_input[0])
        self.total_inputs = self.__input_storage.inputs
        self.input_selection = input_selection
        self.is_end_to_end = is_end_to_end

        # init for the game
        self.__last_game = None
        self.current_input_entry = None
        self.__current_game = None
        self.__done = False
        self.__current_sanitization = None
        self.__is_context_escaped = False
        self.__before_syntax_fixing = False
        self.__current_error = False
        self.__escapes = 0
        

        # reward dict
        self.__reward_score ={
            Game_Type.BEHAVIOR_CHANGING:{
                "in_context":-1,
                "out_context":1,
                "escape_context":-1,
                "unescaped_context":-10,
                "change_behavior":0,
                "unchanged_behavior":-1,
                "win":0,
            },
            Game_Type.SYNTAX_FIXING:{
                "win":0,
                "loss":-1
            },
            Game_Type.SANITIZATION_ESCAPING:{
                "win":0,
                "loss":-1
            },
            Game_Type.DONE:{
                "win":0,
                "loss":0
            }
        }
        pass

    def setup_inputs(self,url):
        '''
            - crawl possible inputs and store them
            - test each input to get corresponding sql statement
            - store results to the input storage
        '''
        possible_inputs = self.__crawler.crawl_possible_inputs(url)
        if len(possible_inputs) == 0:
            print("[!] no possible inputs found")
            sys.exit()
        filtered_inputs, sql_statements = self.__sql_filter.test_for_sql_statement(possible_inputs)
        if len(filtered_inputs) == 0:
            print("[!] no combination inputs and sql found")
            sys.exit()
        self.__input_storage.add_new_inputs(filtered_inputs,sql_statements)


    def reset(self,change_input=False):
        # init for the game
        self.__escapes = 0
        if  (change_input  and not self.__input_storage.is_empty()) or (self.current_input_entry is  None and not self.__input_storage.is_empty() ):

            # select next input based on user policy
            if self.input_selection == 1:
                self.current_input_entry = self.__input_storage.pop_next_input()
            elif self.input_selection == 2:
                self.current_input_entry = self.__input_storage.choose_random_input()
            else:
                self.current_input_entry = self.__input_storage.pop_next_input()

            self.current_input_entry.reset()
            if self.current_input_entry.is_escaped_context():
                self.__current_game = Game_Type.BEHAVIOR_CHANGING
            else:
                self.__current_game = Game_Type.SYNTAX_FIXING
            self.__done = False
            self.__current_sanitization = None
            self.__last_game = None
            self.__is_context_escaped = False
            self.__before_syntax_fixing = None
            self.__current_error = False

        else:
            if change_input:
                raise Exception("no input left")

            # print("[Environment->reset] reset the current input")
            self.current_input_entry.reset()
            if self.current_input_entry.is_escaped_context():
                self.__current_game = Game_Type.BEHAVIOR_CHANGING
            else:
                self.__current_game = Game_Type.SYNTAX_FIXING
            self.__done = False
            self.__current_sanitization = None
            self.__last_game = None
            self.__is_context_escaped = False
            self.__before_syntax_fixing = None
            self.__current_error = False
        state = self.current_state()
        return self.__current_game, state
        
    def step(self,action):
        '''
            apply the action on the input and return game, updated state and reward
        '''
        # print()
        # print("---------------------[Environment]---------------------")
        assert(self.__current_game is not None)

        # validate action
        assert(self.is_valid_action(action))

        # check if input already exploited (game is done)
        if self.__done:
            return self.__current_game, self.current_state(), self.reward(),self.__done

        # apply action on payload and send request
        self.current_input_entry.apply_action(action)

        # check if new sql statement sent and update game type
        new_statement = self.__sql_filter.get_new_sql_statement(self.current_input_entry.input)
        # print(f"[environment->step] new statment seen: {new_statement}")
        if new_statement is not None:
            # update history
            self.current_input_entry.update_sql_history(new_statement)
            self.__current_error = False

            # check if any sanitized elements from input
            if self.current_input_entry.get_next_sanitized_token() is not None:
                sanitized_element = self.current_input_entry.get_next_sanitized_token()
                # print(f"[Environment] found sanatisation element {sanitized_element}")
                self.__last_game = self.__current_game
                self.__current_game = Game_Type.SANITIZATION_ESCAPING
                # print(f"[Environment->step] game changed from {self.__last_game} to {self.__current_game}")
                # input(f"[Environment->step]no error first santize")

            # change game type to behvaior changing if syntax fixing
            elif  not self.current_input_entry.is_escaped_context():
                # assert(self.__last_game != None)
                # switch so reward givin from fixing syntax
                # assert(self.__before_syntax_fixing != None)
                self.__last_game = self.__current_game
                self.__current_game = Game_Type.SYNTAX_FIXING
                self.__before_syntax_fixing = None
                # print(f"[Environment->step] game changed from {self.__last_game} to {self.__current_game}")
                # input(f"[Environment->step] no error syntax not escaped going to syntax 2")

            else:
                self.__escapes +=1
                self.__last_game = self.__current_game
                self.__current_game = Game_Type.BEHAVIOR_CHANGING
                # print(f"[Environment->step] game changed from {self.__last_game} to {self.__current_game}")
                # input(f"[Environment->step] no error behaviour")


            # # if sanitized escaping check if element escape sanitization if it exist and not removed
            # if self.__current_game == Game_Type.SANITIZATION_ESCAPING and not self.current_input_entry.is_payload_token_sanatized(self.__current_sanitization):
            #     self.__current_game = Game_Type.BEHAVIOR_CHANGING
            #     self.__last_game = Game_Type.SANITIZATION_ESCAPING

        else:
            
            # check if any sanitized elements from input
                # change game to syntax fixing
                # assert(self.__current_game != None)
                self.__last_game = self.__current_game
                self.__before_syntax_fixing = self.current_game
                self.__current_game = Game_Type.SYNTAX_FIXING
                self.__current_error = True
                # print(f"[Environment->step] game changed from {self.__last_game} to {self.__current_game}")
                # input(f"[Environment->step] error syntax fixing")


        # check if behavior changed
        if not self.__current_error and self.__current_game is not Game_Type.SANITIZATION_ESCAPING and self.current_input_entry.is_behavior_changed():
            self.__last_game = self.__current_game
            self.__current_game = Game_Type.DONE
            self.__done = True
        # return values  
        return self.__current_game ,self.current_state() ,self.reward() ,self.__done

    def current_game(self):
        return self.__current_game

    def current_state(self):
        '''
            generate current state of the environment from the input
        '''
        assert(self.__current_game is not None and self.current_input_entry is not None)
        state = {}
        # game
        state["game"] = self.__current_game

        # is error 
        state["error"] = self.__current_error

        # get payload
        state["payload"] = self.current_input_entry.payload

        # get sql statment
        state["sql"] = self.current_input_entry.sql_history[-1]

        # available actions
        state["actions"] = self.available_actions()

        # input token
        state["token"] = self.current_input_entry.input.token

        # done
        state["done"] = self.__done
        return state

    def reward(self) -> float:
        '''
            generate reward based on the current state and game
        '''
        assert(self.__current_game is not None and self.current_input_entry is not None)
        # print(f"[Environment->reward] last state {self.__last_game} current_state {self.__current_game}")
        if self.__current_game == Game_Type.BEHAVIOR_CHANGING:
            if self.__last_game == Game_Type.SYNTAX_FIXING:
                # last game was syntax fixing and get fixed
                return -1
            elif self.__last_game == Game_Type.SANITIZATION_ESCAPING:
                #last game was sanatisation and get escaped
                return -1
            else:
                # if context exist
                if self.current_input_entry.is_identifier_in_context():
                    # get number of elements inside context (-ve * number of elements)
                    flat_index_length = len(self.current_input_entry.payload.base_token.flat_idx_tokens_list())
                    in_context_reward = (self.__reward_score[self.__current_game]["in_context"] * len(self.current_input_entry.in_context_elements()))
                    out_context_reward = (self.__reward_score[self.__current_game]["out_context"] * ((1- len(self.current_input_entry.in_context_elements())))/ flat_index_length)
                    # if any context escape element inserted +ve
                    # escape_context = self.__reward_score[self.__current_game]["escape_context"] if self.current_input_entry.is_context_escaped() else self.__reward_score[self.__current_game]["unescaped_context"]

                    # input(f"[Environment->reward] behviour rewards: in context elements ({self.__reward_score[self.__current_game]['in_context']} * {len(self.current_input_entry.in_context_elements())}) / {flat_index_length}= {in_context_reward}, escape context {escape_context}")
                    return -1
                else:
                    change_behviour = self.__reward_score[self.__current_game]["change_behavior"] if self.current_input_entry.is_context_escaped() else self.__reward_score[self.__current_game]["unchanged_behavior"]
                    return -1


        elif self.__current_game == Game_Type.SYNTAX_FIXING:
            # syntax fixing
            flat_index_length = len(self.current_input_entry.payload.base_token.flat_idx_tokens_list())
            in_context_reward = (-1 * len(self.current_input_entry.in_context_elements())) + -1

            return -1


        elif self.__current_game == Game_Type.SANITIZATION_ESCAPING:
            if self.__last_game == Game_Type.SYNTAX_FIXING:
                return -1
            else:
                # sanatisation escaping
                return -1


        elif  self.__current_game == Game_Type.DONE:
            if self.__last_game == Game_Type.SYNTAX_FIXING:
                # last game was syntax fixing and get fixed
                return 0
            elif self.__last_game == Game_Type.SANITIZATION_ESCAPING:
                #last game was sanatisation and get escaped
                return 0
            elif  self.__last_game == Game_Type.BEHAVIOR_CHANGING:
                #last game was behviour and get chnaged
                return 0
            else:
                # done
                return 0
        else:
            assert(False)

        return None

    def available_actions(self):
        '''
            filter out the actions based on game type
            TODO: reduce the number of actions based on sql statement
        '''
        assert(self.__current_game is not None)
        # get payload index of after context if behviour changing
        out_of_context_starting_index = self.current_input_entry.get_starting_out_of_context_payload_index()

        if self.is_end_to_end:

            if out_of_context_starting_index:
                self.current_input_entry.payload.escaped_context = out_of_context_starting_index
                action_game_map = {}
                for current_game in Game_Type.__iter__():
                    action_game_map[current_game] = self.current_input_entry.payload.available_actions(SQLI_Environment.game_to_token[current_game],out_of_context_starting_index)
                return action_game_map
            else:
                action_game_map = {}
                for current_game in Game_Type.__iter__():
                    action_game_map[current_game] = self.current_input_entry.payload.available_actions(SQLI_Environment.game_to_token[current_game])
                return action_game_map
        else:
            if out_of_context_starting_index:
                return self.current_input_entry.payload.available_actions(SQLI_Environment.game_to_token[self.__current_game],out_of_context_starting_index)
            else:
                return self.current_input_entry.payload.available_actions(SQLI_Environment.game_to_token[self.__current_game])        
            
            

    
    def get_all_actions(self,max_timestamp):
        return self.current_input_entry.payload.get_all_actions(max_timestamp)

    def is_valid_action(self,action):
        assert(self.__current_game is not None)
        out_of_context_starting_index = self.current_input_entry.get_starting_out_of_context_payload_index()
        if out_of_context_starting_index:
            return self.current_input_entry.payload.available_actions(SQLI_Environment.game_to_token[self.__current_game],out_of_context_starting_index)
        else:
            return self.current_input_entry.payload.available_actions(SQLI_Environment.game_to_token[self.__current_game])
