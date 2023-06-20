import random

from Environment.Tokens_Actions.Basic_Block.Base_Token import Base_Token
from Environment.Tokens_Actions.Basic_Block.Comma_Token import Comma_Token
from Environment.Tokens_Actions.Basic_Block.CommentRange_Token import CommentRange_Token
from Environment.Tokens_Actions.Basic_Block.Comment_Token import Comment_Token
from Environment.Tokens_Actions.Basic_Block.FullComment_Token import FullComment_Token
from Environment.Tokens_Actions.Basic_Block.HexRepresentation_Token import HexRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.IdentifierRepresentation_Token import IdentifierRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Identifier_Token import Identifier_Token
from Environment.Tokens_Actions.Basic_Block.KeywordRepresentation_Token import KeywordRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.Paranthesis_Token import Paranthesis_Token
from Environment.Tokens_Actions.Basic_Block.Quote_Token import Quote_Token
from Environment.Tokens_Actions.Basic_Block.Slash_Token import Slash_Token
from Environment.Tokens_Actions.Basic_Block.StringRepresentation_Token import StringRepresentation_Token
from Environment.Tokens_Actions.Basic_Block.String_Token import String_Token
from Environment.Tokens_Actions.Basic_Block.Token import Token
from Environment.Tokens_Actions.Basic_Block.Whitespace_Token import Whitespace_Token
from Environment.Tokens_Actions.Behavior_Changing.AND_Token import AND_Token
from Environment.Tokens_Actions.Behavior_Changing.IF_Token import IF_Token
from Environment.Tokens_Actions.Behavior_Changing.OR_Token import OR_Token
from Environment.Tokens_Actions.Behavior_Changing.SLEEP_Token import SLEEP_Token
from Environment.Tokens_Actions.Behavior_Changing.UNION_Token import UNION_Token
from Environment.Tokens_Actions.Behavior_Changing.WHERE_Token import WHERE_Token
from Environment.Tokens_Actions.Sanitization_Escaping.CONCAT_Token import CONCAT_Token
from Environment.Tokens_Actions.Sanitization_Escaping.Capatlize_Action import Capatilize_Action
from Environment.Tokens_Actions.Sanitization_Escaping.Represerntation_Action import Representation_Action
from Environment.Tokens_Actions.Sanitization_Escaping.WhitespaceConverter_Action import WhitespaceConverter_Action
from Environment.Tokens_Actions.Syntax_Fixing.StringGeneration_Action import StringGeneration_Action

actions= ["add_comma","add_comment","comment_range","add_paranthesis","add_quote","add_whitespace","add_string",\
          "add_and","add_or","add_if","add_sleep","add_union","add_where",\
          "capatilize_keyword","convert_str_char","convert_str_hex","convert_str_concat","change_non_whitespace",\
          "remove_token","convert AND to &", "add null byte to quote"]

idx_to_action_map = {i:curr_action for i,curr_action in enumerate(actions)}
action_to_idx_map = {curr_action:i for i,curr_action in enumerate(actions)}
class Payload:
    def __init__(self,identifier) -> None:
        self.sleep_time = 20
        self.max_time = 50
        self.max_token =50
        self.base_token = Base_Token()
        self.identifier = identifier
        self.identifier_token = IdentifierRepresentation_Token(identifier)
        self.base_token.append_token_base_idx(self.identifier_token)
        self.escaped_context = None
        pass

    def apply_action(self,action_payload:list):
        '''
            apply action on token based on type of action supplied
            - parameter:
                - action -> action list [action type, [parameters]]
                
        '''
        
        action = action_payload["action"]
        range = action_payload["range"]
        type = action_payload["type"]
        # validate action
        assert(action in idx_to_action_map.keys())
        assert(isinstance(range,list))

        # apply action
        
        if action == 0:# add comma
            # get pos 
            pos = range[0]
            # validate pose
            assert(self.base_token.is_valid_append_base_idx(pos))

            # add comma token at pos
            comma_token = Comma_Token()
            self.base_token.insert_token_base_idx(comma_token,pos)
        elif action == 1:# add comment
            # get pos, type
            pos = range[0]

            # validate type
            assert(Comment_Token.is_valid_type(type))

            # add comment token at pos
            flat_end_index = self.base_token.base_idx_length()
            assert(self.base_token.is_valid_append_base_idx_range(pos,flat_end_index))
            tokens = self.base_token.get_tokens_list_base_idx(pos,flat_end_index)

            comment_token = FullComment_Token(type,[])
            self.base_token.insert_token_base_idx(comment_token,pos)

        elif action == 2:# add comment range
            # get pos start, pos end
            pos_start = range[0]
            pos_end = range[1]

            # validate pos_start and pos_end
            assert(self.base_token.is_valid_append_base_idx_range(pos_start,pos_end))

            # get token list
            tokens = self.base_token.get_tokens_list_base_idx(pos_start,pos_end)

            # add comment range token
            comment_range_token = CommentRange_Token(tokens,type)
            self.base_token.replace_range_tokens_base_idx(pos_start,pos_end,comment_range_token)
        elif action == 3:#add paranthesis
            # get pos, type
            pos = range[0]

            # validate pos, type
            assert(self.base_token.is_valid_append_base_idx(pos))
            assert(Paranthesis_Token.is_valid_type(type))

            # add paranthesis token
            paranthesis_token = Paranthesis_Token(type)
            self.base_token.insert_token_base_idx(paranthesis_token,pos)
        elif action == 4:# add quote
            # get pos, type
            pos = range[0]

            # validate pos, type
            assert(self.base_token.is_valid_append_base_idx(pos))
            assert(Quote_Token.is_valid_type(type))

            # add quote token
            quote_token = Quote_Token(type)
            self.base_token.insert_token_base_idx(quote_token,pos)


        elif action == 5:# add whitespace
            # get pos, type
            pos = range[0]

            # validate pos, type
            assert(self.base_token.is_valid_append_base_idx(pos))
            assert(Whitespace_Token.is_valid_type(type))

            # add whitespace token
            whitespace_token = Whitespace_Token(type)
            self.base_token.insert_token_base_idx(whitespace_token,pos)
        elif action == 6:#add string
            # get pos
            pos = range[0]

            # validate pos
            assert(self.base_token.is_valid_append_base_idx(pos))

            # add if token
            string_token = StringGeneration_Action.generate_string()
            self.base_token.insert_token_base_idx(string_token,pos)

        elif action == 7:# add and 
            # get pos
            pos = range[0]

            # validate pos
            assert(self.base_token.is_valid_append_base_idx(pos))

            # add and token
            and_token = AND_Token()
            self.base_token.insert_token_base_idx(and_token,pos)
        elif action == 8:# add or
            # get pos
            pos = range[0]

            # validate pos
            assert(self.base_token.is_valid_append_base_idx(pos))

            # add or token
            or_token = OR_Token()
            self.base_token.insert_token_base_idx(or_token,pos)
        elif action == 9:# add if 
            # get pos
            pos = range[0]

            # validate pos
            assert(self.base_token.is_valid_append_base_idx(pos))

            # add if token
            if_token = IF_Token()
            self.base_token.insert_token_base_idx(if_token,pos)
        elif action == 10:#add sleep
            # get pos, time
            pos = range[0]
            time = 20

            # validate pos, time
            assert(self.base_token.is_valid_append_base_idx(pos))
            assert(time > 0 and time <= self.max_time)

            # add sleep token
            sleep_token = SLEEP_Token(time)
            self.base_token.insert_token_base_idx(sleep_token,pos)
        elif action == 11:#add union
            # get pos
            pos = range[0]

            # validate pos
            assert(self.base_token.is_valid_append_base_idx(pos))

            # add if token
            union_token = UNION_Token()
            self.base_token.insert_token_base_idx(union_token,pos)

        elif action == 12:#add where
            # get pos
            pos = range[0]

            # validate pos
            assert(self.base_token.is_valid_append_base_idx(pos))

            # add if token
            where_token = WHERE_Token()
            self.base_token.insert_token_base_idx(where_token,pos)

        elif action == 13:#capitalize keyword randomly
            # get pos
            pos = range[0]

            # validate
            assert(self.base_token.is_valid_flat_idx(pos))
            assert(self.base_token.is_keyword_flat_idx(pos))

            # capatilze randomly the keyword
            keyword = self.base_token.get_token_flat_idx(pos)
            Capatilize_Action.captilize_keyword_randomly(keyword)

        elif action == 14:# convert str to char
            # get pos
            pos = range[0]

            # validate 
            assert(self.base_token.is_valid_flat_idx(pos-1))
            assert(self.base_token.is_valid_flat_idx(pos))
            assert(self.base_token.is_valid_flat_idx(pos+1))


            # convert str to char
            string = self.base_token.get_token_flat_idx(pos)   
            token = Representation_Action.str_to_char(string)
            # remove quote before and after
            self.base_token.remove_token_flat_idx(pos-1)
            self.base_token.remove_token_flat_idx(pos)
            self.base_token.replace_flat_idx(pos-1,token)

        elif action == 15:# convert str to hex
            # get pos
            pos = range[0]

            # validate 
            assert(self.base_token.is_valid_flat_idx(pos))
            assert(self.base_token.is_string_flat_idx(pos))

            # convert str to hex
            string = self.base_token.get_token_flat_idx(pos)    
            token = Representation_Action.str_to_hex(string)
            # remove quote before and after
            self.base_token.remove_token_flat_idx(pos-1)
            self.base_token.remove_token_flat_idx(pos)
            self.base_token.replace_flat_idx(pos-1,token)
        elif action == 16:# convert str to concat
            # get pos, type
            pos = range[0]
            # validate 
            assert(self.base_token.is_valid_flat_idx(pos))
            assert(self.base_token.is_string_flat_idx(pos))
            assert(CONCAT_Token.is_valid_type(type))

            # convert str to concat
            string = self.base_token.get_token_flat_idx(pos)     
            string_value = string.value()
            string_length = (len(string_value)//2) - 1
            string_1 = string_value[0:string_length]
            string_2 = string_value[string_length:]
            quote_type = random.randint(0,len(Quote_Token.quote_type_mapping.keys())-1)
            token = CONCAT_Token(type,[String_Token(string_1,quote_type),String_Token(string_2,quote_type)])
            # remove quote before and after
            self.base_token.remove_token_flat_idx(pos-1)
            self.base_token.remove_token_flat_idx(pos)
            self.base_token.replace_flat_idx(pos-1,token)
            
        elif action == 17:# change whitespace to non whitespace
            # get pos, type
            pos = range[0]

            # validate 
            assert(self.base_token.is_valid_append_base_idx(pos))

            # convert whitespace to non whitespace
            and_oper = self.base_token.token_list[pos]
            and_oper.change_whitespace_type(1)
            
        elif action == 18:# remove token
            # get pos 
            pos = range[0]
            # validate pose
            assert(self.base_token.is_valid_append_base_idx(pos))
            # remove token at pos
            self.base_token.remove_token_base_idx(pos)

        elif action == 19:#change and to &
            # get pos, type
            pos = range[0]

            # validate 
            assert(self.base_token.is_valid_append_base_idx(pos))

            # convert whitespace to non whitespace
            and_oper = self.base_token.token_list[pos]
            and_oper.change_type(1)
            #print(self)
        elif action == 20:#add slash before quote
            # get pos, type
            pos = range[0]
            # validate 
            assert(self.base_token.is_valid_flat_idx(pos))
            slash = Slash_Token()
            self.base_token.replace_flat_idx_token_with_tokens(pos,[slash,self.base_token.get_token_flat_idx(pos)])
        else:# invalid action
            assert(False,"invalid action")
        
        
    def available_actions(self,action_category:list,out_of_contex_starting_index=None):
        # validate given category
        assert(all([isinstance(current,Token.Category) for current in action_category]))
        # return actions possible for the payload
        actions = []
        # get base number of tokens
        no_tokens = self.base_token.base_idx_length()
        # get flat number of tokens
        no_flat_tokens = self.base_token.flat_idx_length()
        if self.escaped_context is not None:
            if self.escaped_context == 0:
                self.escaped_context = 1
            # print(f"[Payload] starting index found {self.escaped_context}")
        starting_index = self.escaped_context if self.escaped_context is not None else 1
            
        if  Token.Category.SYNTAX_FIXING in action_category:
            
            # add comment type 0
            for current_pos in range(1,no_tokens+1):
                if current_pos < no_tokens and isinstance(self.base_token.token_list[current_pos],FullComment_Token):
                    break
                else:
                    actions.append({"action":1,"range":[current_pos,current_pos],"type":0})

            # # add paranthesis type 1
            for current_pos in range(1,no_tokens+1):
                if current_pos < no_tokens and isinstance(self.base_token.token_list[current_pos],FullComment_Token):
                    actions.append({"action":3,"range":[current_pos,current_pos],"type":1})
                    break
                actions.append({"action":3,"range":[current_pos,current_pos],"type":1})

            # # add quote type 0
            for current_pos in range(1,no_tokens+1):
                if current_pos < no_tokens and isinstance(self.base_token.token_list[current_pos],FullComment_Token):
                    actions.append({"action":4,"range":[current_pos,current_pos],"type":0})
                    break
                actions.append({"action":4,"range":[current_pos,current_pos],"type":0})

            # # add quote type 1
            for current_pos in range(1,no_tokens+1):
                if current_pos < no_tokens and isinstance(self.base_token.token_list[current_pos],FullComment_Token):
                    actions.append({"action":4,"range":[current_pos,current_pos],"type":1})
                    break
                actions.append({"action":4,"range":[current_pos,current_pos],"type":1})

            # # add quote type 3
            for current_pos in range(1,no_tokens+1):
                if current_pos < no_tokens and isinstance(self.base_token.token_list[current_pos],FullComment_Token):
                    actions.append({"action":4,"range":[current_pos,current_pos],"type":2})
                    break
                actions.append({"action":4,"range":[current_pos,current_pos],"type":2})    

            # remove token
            for current_pos in range(1,no_tokens):
                if not isinstance(self.base_token.token_list[current_pos],IdentifierRepresentation_Token):
                    actions.append({"action":18,"range":[current_pos,current_pos],"type":0})

        if Token.Category.SYNTAX_FIXING in action_category or Token.Category.BEHAVIOR_CHANGING in action_category:
           
            
            # add and token
            for current_pos in range(1,no_tokens+1):
                
                if (current_pos < no_tokens and isinstance(self.base_token.token_list[current_pos],AND_Token)) or (current_pos-1 >= 0 and isinstance(self.base_token.token_list[current_pos-1],AND_Token)):
                    pass
                elif current_pos < no_tokens and isinstance(self.base_token.token_list[current_pos],FullComment_Token):
                    actions.append({"action":7,"range":[current_pos,current_pos],"type":0})
                    break
                else: 
                    actions.append({"action":7,"range":[current_pos,current_pos],"type":0})

            # remove token
            for current_pos in range(no_tokens):
                 if not isinstance(self.base_token.token_list[current_pos],IdentifierRepresentation_Token) and self.base_token.token_list[current_pos].category() == Token.Category.BEHAVIOR_CHANGING:
                     actions.append({"action":18,"range":[current_pos,current_pos],"type":0})
        if Token.Category.SANATISATION_ESCAPING in action_category or Token.Category.SYNTAX_FIXING in action_category:

            # capitalise random pos
            for current_pos in range(no_flat_tokens):
                if isinstance(self.base_token.get_token_flat_idx(current_pos),KeywordRepresentation_Token) and self.base_token.get_token_flat_idx(current_pos).is_all_caps():
                    actions.append({"action":13,"range":[current_pos,current_pos],"type":0})
            
            # # change whitespace
            for current_pos in range(no_tokens):
                token = self.base_token.token_list[current_pos]

                if isinstance(token,AND_Token) and token.whitespace_type_value() == 0:
                    actions.append({"action":17,"range":[current_pos,current_pos],"type":0})
            
            # change and operation to &
            for current_pos in range(no_tokens):
                token = self.base_token.token_list[current_pos]

                if isinstance(token,AND_Token) and token.type_value() == 0:
                    actions.append({"action":19,"range":[current_pos,current_pos],"type":0})

            
            # remove token
            for current_pos in range(no_tokens):
                if not isinstance(self.base_token.token_list[current_pos],IdentifierRepresentation_Token):
                    actions.append({"action":18,"range":[current_pos,current_pos],"type":0})
            pass
        return actions

    def get_all_actions(self,max_timstamp):
        all_actions = {}
        for current_timestamp in range(max_timstamp*4):
            all_actions[str([1,current_timestamp,0])] = [0 for x in range(max_timstamp)]
            all_actions[str([3,current_timestamp,1])] = [0 for x in range(max_timstamp)]
            all_actions[str([4,current_timestamp,0])] = [0 for x in range(max_timstamp)]
            all_actions[str([4,current_timestamp,1])] = [0 for x in range(max_timstamp)]
            all_actions[str([4,current_timestamp,2])] = [0 for x in range(max_timstamp)]
            all_actions[str([18,current_timestamp,0])] = [0 for x in range(max_timstamp)]
            all_actions[str([7,current_timestamp,0])] = [0 for x in range(max_timstamp)]
            all_actions[str([13,current_timestamp,0])] = [0 for x in range(max_timstamp)]
            all_actions[str([17,current_timestamp,0])] = [0 for x in range(max_timstamp)]
            all_actions[str([19,current_timestamp,0])] = [0 for x in range(max_timstamp)]
            all_actions[str([20,current_timestamp,0])] = [0 for x in range(max_timstamp)]

        return all_actions
            

    def reset(self):
        self.base_token = Base_Token()
        identifier_token = IdentifierRepresentation_Token(self.identifier)
        self.base_token.append_token_base_idx(identifier_token)
        self.escaped_context = None

    def is_valid_action(self,action,action_category,out_of_context_index=None):
        return action in self.available_actions(action_category,out_of_context_index)

    def is_valid_flat_index(self,flat_index):
        return self.base_token.is_valid_flat_idx(flat_index)

    def is_valid_base_index(self,base_index):
        return self.base_token.is_valid_base_idx(base_index)

    def get_token_flat_idx(self,flat_index):
        assert(self.is_valid_flat_index(flat_index))
        return self.base_token.get_token_flat_idx(flat_index)

    def get_tokens_flat_idx(self):
        return self.base_token.flat_idx_tokens_list()

    def get_tokens_base_idx(self):
        return self.base_token.token_list

    def __str__(self) -> str:
        return str(self.base_token)