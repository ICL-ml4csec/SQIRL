import pprint
import random
from typing import Tuple, Union
from Environment.Input.Input import Input
from Environment.Payload.Payload import Payload
from Environment.SQL.SQL import SQL
from Environment.Tokens_Actions.Basic_Block.IdentifierRepresentation_Token import IdentifierRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
import os
from copy import copy
class Input_storage:

    def __init__(self) -> None:
        self.__storage = []
        self.inputs = len(self.__storage)
        pass

    def add_new_inputs(self,filtered_inputs,sql_statments):
        '''
            - create new entry of input with coresponding sql and initlize payload with token
            - add inputs to the list to be explored
        '''
        # log all combination in logs
        inputs_found = open(os.path.join("stats_logs","all_inputs_found.stat"),"w+")
        for current_index, current_input_current_sql in enumerate(list(zip(filtered_inputs,sql_statments))):
            current_input, current_sql = (current_input_current_sql[0],current_input_current_sql[1])
            inputs_found.write(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%{current_index}%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")
            inputs_found.write(f"input action: {current_input.action}\n")
            inputs_found.write(f"input method: {current_input.method}\n")
            inputs_found.write(f"input inputs: {current_input.inputs}\n")
            inputs_found.write(f"input parent_link: {current_input.parent_link}\n")
            inputs_found.write(f"SQL statment: {current_sql.sql_statment}\n\n")
            
        new_entries = [Entry(current_input,current_sql_stmt,Payload(current_input.token)) for current_input,current_sql_stmt in zip(filtered_inputs,sql_statments)]
        self.__storage.extend(new_entries)
        self.inputs = len(self.__storage)
        pass 

    def pop_next_input(self):
        '''
            pop next input in FIFO 
        '''
        assert(not self.is_empty())
        self.inputs = len(self.__storage) - 1
        next_input = copy(self.__storage[0])
        self.__storage = self.__storage[-self.inputs:]
        # print("[Input_storage->pop_next_input] pop next input from storage")
        return next_input

    def manual_select_input(self):
        assert(not self.is_empty())
        pp = pprint.PrettyPrinter(indent=4)
        self.inputs = len(self.__storage) - 1
        for i,current_input in enumerate(self.__storage):
            print(i)
            pp.pprint(current_input.input.action)
            pp.pprint(current_input.sql_history[0])
            print()

        found = True
        while(found):
            try:
                value = int(input("choose input"))

                if value < len(self.__storage) and value >= 0:
                    found = False
                else:
                    found = True
            except:
                found = True
        return self.__storage[value]

    def choose_random_input(self):
        self.inputs = len(self.__storage) - 1
        return random.choice(self.__storage)

    def is_empty(self):
        '''
            check if storage is empty
        '''
        return len(self.__storage) == 0


class Entry:
    '''
        class used to store the input and its coresponding sql history and payload
    '''
    def __init__(self,input:Input,sql_stmt:SQL,payload:Payload) -> None:
        self.input = input
        self.sql_history = [sql_stmt]
        self.payload = payload
        pass

    def apply_action(self,action):
        # print(f"[input_storage->apply_action] applying action {action}")
        # apply action on payload
        self.payload.apply_action(action)
        # print(f"[input_storage->apply_action] payload after action {self.payload}")
        # send payload request via input
        self.input.send_request(self.payload)

    def update_sql_history(self,new_statement:SQL):
        # print(new_statement)
        self.sql_history.append(new_statement)

    def is_valid_action(self,action,game_Type):
        '''
            check if the action is available to be applied on payload
        '''
        return self.payload.is_valid_action(action,game_Type)

    def is_payload_token_sanatized(self,paylaod_flat_token_idx:int) -> Union[int,None]:
        '''
            check if given index of payload flat index token is sanatized
        '''
        return self.sql_history[-1].is_sanatized(self.payload,paylaod_flat_token_idx)

    def get_next_sanitized_token(self) -> Union[int,None]:
        '''
            compares each payload token with its supposed corseponding place and return when token is not found along with its replaced token
            we assume identiefier must exist and cant be santized
        '''
        # get sql from history

        # get payload tokens flat index
        payload_flat_tokens = self.payload.base_token.flat_idx_tokens_list()

        # identifer index
        payload_flat_identifier_index = -1
        # check each token after passing the identifier token wether it is santized or not
        for i,current_payload_flat_token in enumerate(payload_flat_tokens):
            if payload_flat_identifier_index == -1:
                if isinstance(payload_flat_tokens[i],IdentifierRepresentation_Token):
                    # print(f"[get_next_sanitized_payload_token] found identifer {current_payload_flat_token} at {i}")
                    payload_flat_identifier_index = current_payload_flat_token
                continue
            else:
                # print(f"[get_next_sanitized_payload_token] check if {current_payload_flat_token} at {i} santized")
                is_santized = self.is_payload_token_sanatized(i)
                if is_santized:
                    return is_santized

        assert(payload_flat_identifier_index != -1)
        return None
 
    def is_escaped_context(self):
        '''
            check if any of the behavior changing tokens are outside the context of the identifier
        '''
        # get last sql statement
        sql_statement = self.sql_history[-1]

        # get all tokens base idx
        tokens = self.payload.get_tokens_base_idx()

        # check if any of the behavior changers tokens are outside the identifier context with respect to the sql tokens
        str_1 = self.payload.identifier_token
        identifier_token_index = -1
        for current_token_idx in range((len(tokens))):
            if tokens[current_token_idx] == self.payload.identifier_token:
                identifier_token_index = current_token_idx

        # print(f"[Input_entry->is_escaped_context] identifier token index {identifier_token_index}")
        assert(identifier_token_index >= 0)

        for current_token_idx in range(len(tokens)):
            # print(f"[is_behavior_changed] check if behavior change between {self.payload.identifier_token} and {tokens[current_token_idx]}")

            if (sql_statement.is_affective_behviour_changing(self.payload,identifier_token_index,current_token_idx)):
                # print(f"[is_behavior_changed]  behavior have been changed between {self.payload.identifier_token} and {tokens[current_token_idx]}")
                return True

    def is_behavior_changed(self):
        '''
            check if any of the behavior changing tokens are outside the context of the identifier
        '''
        # get last sql statement
        sql_statement = self.sql_history[-1]

        # get all tokens base idx
        tokens = self.payload.get_tokens_base_idx()

        # check if any of the behavior changers tokens are outside the identifier context with respect to the sql tokens
        str_1 = self.payload.identifier_token
        identifier_token_index = -1
        for current_token_idx in range((len(tokens))):
            if tokens[current_token_idx] == self.payload.identifier_token:
                identifier_token_index = current_token_idx

        # print(f"[Input_Entry->is_behavior_changed] identifier token index {identifier_token_index}")
        assert(identifier_token_index >= 0)
        current_token_idx += 1
        for current_token_idx in range(len(tokens)):
            # print(f"[Input_Entry->is_behavior_changed] check if behavior change between {self.payload.identifier_token} and {tokens[current_token_idx]}")

            if ((sql_statement.is_affective_behviour_changing(self.payload,identifier_token_index,current_token_idx) and tokens[current_token_idx].category() == Token.Category.BEHAVIOR_CHANGING)) or sql_statement.is_keyword_after_payload_commented(self.payload,identifier_token_index):
                # print(f"[Input_Entry->is_behavior_changed]  behavior have been changed between {self.payload.identifier_token} and {tokens[current_token_idx]}")
                return True
        # print(f"[Input_Entry->is_behavior_changed] no behavior changing")

        return False
    def get_starting_out_of_context_payload_index(self):
        '''
            check if any of the behavior changing tokens are outside the context of the identifier
        '''
        # get last sql statement
        sql_statement = self.sql_history[-1]

        # get all tokens base idx
        tokens = self.payload.get_tokens_base_idx()

        # check if any of the behavior changers tokens are outside the identifier context with respect to the sql tokens
        str_1 = self.payload.identifier_token
        identifier_token_index = -1
        for current_token_idx in range((len(tokens))):
            if tokens[current_token_idx] == self.payload.identifier_token:
                identifier_token_index = current_token_idx

        # print(f"[Input_Entry->get_starting_out_of_context_payload_index] identifier token index {identifier_token_index}")
        assert(identifier_token_index >= 0)

        for current_token_idx in range(len(tokens)):
            # print(f"[Input_Entry->get_starting_out_of_context_payload_index] check if behavior change between {self.payload.identifier_token} and {tokens[current_token_idx]}")

            if (sql_statement.is_affective_behviour_changing(self.payload,identifier_token_index,current_token_idx)):
                # print(f"[Input_Entry->get_starting_out_of_context_payload_index]  behavior have been changed between {self.payload.identifier_token} and {tokens[current_token_idx]}")
                return current_token_idx
        # print(f"[Input_Entry->get_starting_out_of_context_payload_index] no behavior changing")

        return None
    def is_identifier_in_context(self)->bool:
        '''
            return true if there is quote context between the identifer
        '''
        # get last sql statement
        sql_statement = self.sql_history[-1]
        return sql_statement.is_identifier_in_context()

    def in_context_elements(self)->list:
        '''
            get the elements after identifer and before the closing quote of the identifier
        '''
        # get last sql statement
        sql_statement = self.sql_history[-1]
        return sql_statement.in_context_elements()

    def is_context_escaped(self)->bool:
        '''
            check if a quote same as identifer closing quote is within the payload
        '''
        # get last sql statement
        sql_statement = self.sql_history[-1]
        # closing quote
        closing_quote = sql_statement.get_identifier_closing_quote()
        # get payload tokens flat index
        payload_flat_tokens = self.payload.base_token.flat_idx_tokens_list()
        # loop through the payload and check if any quote same as the closing quote
        for current_token in payload_flat_tokens:
            if len(closing_quote) > 0:
                if str(current_token) == closing_quote[0]:
                    closing_quote.pop(0)
            else:
                return True

        return False
    def get_number_of_behviour_changing(self):
        # get payload base
        paylod_base_tokens = self.payload.get_tokens_base_idx()

        # iterate to find all behviour changing
        behviour_Changing = 0
        for current_token in paylod_base_tokens:
            if current_token.category() == Token.Category.BEHAVIOR_CHANGING:
                behviour_Changing += 1
        return behviour_Changing
    def reset(self):
        '''
            reset the state of the input
        '''
        # print("[input_storage->entry->reset] reset current entry to init")
        self.sql_history = [self.sql_history[0]]
        self.payload.reset()
        self.input.reset()


